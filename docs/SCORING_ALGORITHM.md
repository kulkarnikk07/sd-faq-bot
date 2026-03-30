# Scoring Algorithm Explainer
## San Diego Permit FAQ Bot

**Version:** 2.0.0  
**Date:** March 2026

---

## Overview

While the San Diego Permit FAQ Bot primarily uses AI (Claude Sonnet 4.6) for generating responses, several scoring and ranking mechanisms work behind the scenes to ensure accurate, relevant answers.

---

## Table of Contents

1. [Permit Relevance Scoring](#permit-relevance-scoring)
2. [Context Prioritization](#context-prioritization)
3. [Response Quality Metrics](#response-quality-metrics)
4. [Cost Estimation Algorithm](#cost-estimation-algorithm)
5. [Timeline Calculation](#timeline-calculation)
6. [Neighborhood Matching](#neighborhood-matching)

---

## 1. Permit Relevance Scoring

### Purpose
Rank permits by relevance to user's query to include the most useful examples in the AI context.

### Algorithm

```python
def score_permit_relevance(user_query: str, permit: Dict) -> float:
    """
    Score a permit's relevance to user query
    
    Returns: 0.0 (irrelevant) to 100.0 (highly relevant)
    """
    
    score = 0.0
    query_lower = user_query.lower()
    query_terms = set(query_lower.split())
    
    # 1. Exact match in permit type (40 points)
    permit_type = permit.get('approval_type', '').lower()
    if query_lower in permit_type:
        score += 40.0
    elif any(term in permit_type for term in query_terms):
        score += 20.0
    
    # 2. Match in project title (30 points)
    project_title = permit.get('project_title', '').lower()
    if query_lower in project_title:
        score += 30.0
    elif any(term in project_title for term in query_terms):
        score += 15.0
    
    # 3. Match in work description (20 points)
    work_desc = permit.get('work_description', '').lower()
    matching_terms = sum(1 for term in query_terms if term in work_desc)
    score += (matching_terms / len(query_terms)) * 20.0
    
    # 4. Recency bonus (10 points)
    issue_date = permit.get('date_approval_issue', '')
    if issue_date:
        days_old = calculate_days_since(issue_date)
        if days_old < 365:  # Within 1 year
            score += 10.0 * (1 - days_old / 365)
    
    return min(score, 100.0)
```

### Example

**Query:** "build a fence"

**Permit A:**
- Type: "Fence Permit"
- Title: "Install 6-foot wooden fence"
- Score: 40 (type match) + 30 (title match) + 15 (description) + 5 (recent) = **90 points**

**Permit B:**
- Type: "Building Permit"
- Title: "Residential addition"
- Description: "includes new fence around property"
- Score: 0 + 0 + 7 (partial description match) + 3 (recent) = **10 points**

**Result:** Permit A ranked higher → included in AI context

---

## 2. Context Prioritization

### Purpose
Determine which data to include in Claude's context window (limited to ~200K tokens).

### Priority Levels

```python
CONTEXT_PRIORITY = {
    'user_query': 1,              # Always included (highest priority)
    'recent_permits': 2,           # Top 10 relevant permits
    'permit_statistics': 3,        # Summary stats
    'municipal_code': 4,           # Relevant code sections
    'neighborhood_info': 5,        # If mentioned in query
    'historical_permits': 6,       # Older examples (if space)
}
```

### Algorithm

```python
def build_context(user_query: str, max_tokens: int = 150000) -> str:
    """
    Build context within token limits
    """
    
    context_parts = []
    current_tokens = 0
    
    # 1. User query (always)
    query_text = f"User Question: {user_query}"
    context_parts.append(query_text)
    current_tokens += estimate_tokens(query_text)
    
    # 2. Relevant permits (top 10)
    permits = search_and_score_permits(user_query, limit=10)
    permits_text = format_permits(permits)
    permits_tokens = estimate_tokens(permits_text)
    
    if current_tokens + permits_tokens < max_tokens:
        context_parts.append(permits_text)
        current_tokens += permits_tokens
    else:
        # Include fewer permits if needed
        permits = permits[:5]
        permits_text = format_permits(permits)
        context_parts.append(permits_text)
        current_tokens += estimate_tokens(permits_text)
    
    # 3. Statistics (if space)
    stats = get_permit_statistics()
    stats_text = format_statistics(stats)
    stats_tokens = estimate_tokens(stats_text)
    
    if current_tokens + stats_tokens < max_tokens:
        context_parts.append(stats_text)
        current_tokens += stats_tokens
    
    # 4. Municipal code (if space)
    if pdf_content and current_tokens < max_tokens * 0.8:
        code_text = get_relevant_code_sections(user_query)
        code_tokens = estimate_tokens(code_text)
        
        if current_tokens + code_tokens < max_tokens:
            context_parts.append(code_text)
            current_tokens += code_tokens
    
    return "\n\n".join(context_parts)
```

### Token Estimation

```python
def estimate_tokens(text: str) -> int:
    """
    Estimate token count
    Rule of thumb: 1 token ≈ 0.75 words ≈ 4 characters
    """
    return len(text) // 4
```

---

## 3. Response Quality Metrics

### Purpose
Evaluate if AI responses meet quality standards.

### Quality Score Components

```python
def calculate_response_quality(response: str, query: str) -> float:
    """
    Score response quality (0-100)
    """
    
    score = 0.0
    
    # 1. Length appropriateness (20 points)
    word_count = len(response.split())
    if 50 <= word_count <= 500:
        score += 20.0
    elif word_count < 50:
        score += 10.0  # Too short
    elif word_count > 500:
        score += 15.0  # Verbose but acceptable
    
    # 2. Keyword coverage (20 points)
    query_keywords = extract_keywords(query)
    keywords_mentioned = sum(1 for kw in query_keywords if kw in response.lower())
    score += (keywords_mentioned / len(query_keywords)) * 20.0
    
    # 3. Structure (20 points)
    has_sections = bool(re.search(r'#{1,3}\s', response))  # Markdown headers
    has_lists = bool(re.search(r'^\s*[-*]\s', response, re.MULTILINE))
    
    if has_sections and has_lists:
        score += 20.0
    elif has_sections or has_lists:
        score += 10.0
    
    # 4. Specificity (20 points)
    # Check for specific details (numbers, names, codes)
    has_numbers = bool(re.search(r'\d+', response))
    has_permit_refs = bool(re.search(r'permit|approval|code', response.lower()))
    has_costs = bool(re.search(r'\$\d+', response))
    
    specificity = sum([has_numbers, has_permit_refs, has_costs]) / 3
    score += specificity * 20.0
    
    # 5. Call to action (20 points)
    # Good responses suggest next steps
    has_cta = any(phrase in response.lower() for phrase in [
        'contact', 'call', 'visit', 'apply', 'submit', 'next step'
    ])
    
    if has_cta:
        score += 20.0
    
    return min(score, 100.0)
```

### Example Scoring

**Good Response (Score: 90):**
```
To build a 6-foot fence in San Diego:

## Required Permits
- Building Permit: $150-300
- Zoning review if near property line

## Timeline
- Application: 1-2 weeks
- Review: 2-3 weeks
- Total: 3-5 weeks

## Next Steps
1. Contact Development Services: (619) 446-5000
2. Submit application with plot plan
```

- Length: 70 words ✓ (20 pts)
- Keywords: fence, permit, timeline ✓ (20 pts)
- Structure: headers + list ✓ (20 pts)
- Specificity: costs, phone number ✓ (20 pts)
- Call to action: contact, submit ✓ (20 pts)
- **Total: 100 points**

**Poor Response (Score: 40):**
```
You need a permit for a fence. Contact the city.
```

- Length: 10 words ✗ (10 pts)
- Keywords: fence, permit ✓ (13 pts)
- Structure: none ✗ (0 pts)
- Specificity: none ✗ (7 pts)
- Call to action: contact ✓ (10 pts)
- **Total: 40 points**

---

## 4. Cost Estimation Algorithm

### Purpose
Estimate permit costs based on historical data.

### Algorithm

```python
def estimate_permit_cost(project_description: str, permit_type: str) -> Dict:
    """
    Estimate permit costs
    
    Returns:
    {
        'min': float,
        'max': float,
        'average': float,
        'confidence': float  # 0-100
    }
    """
    
    # 1. Get historical permits of this type
    similar_permits = search_permits(permit_type, limit=100)
    
    # 2. Extract valuation data
    valuations = [
        float(p['approval_valuation']) 
        for p in similar_permits 
        if p.get('approval_valuation') and float(p['approval_valuation']) > 0
    ]
    
    if not valuations:
        return {
            'min': 100,
            'max': 1000,
            'average': 500,
            'confidence': 20  # Low confidence
        }
    
    # 3. Calculate statistics
    min_cost = np.percentile(valuations, 10)  # 10th percentile
    max_cost = np.percentile(valuations, 90)  # 90th percentile
    avg_cost = np.median(valuations)
    
    # 4. Adjust for project complexity
    complexity_multiplier = 1.0
    
    if 'major' in project_description.lower():
        complexity_multiplier = 1.5
    elif 'minor' in project_description.lower():
        complexity_multiplier = 0.7
    
    # 5. Calculate confidence
    sample_size = len(valuations)
    confidence = min(sample_size / 100 * 100, 100)  # More samples = higher confidence
    
    return {
        'min': min_cost * complexity_multiplier,
        'max': max_cost * complexity_multiplier,
        'average': avg_cost * complexity_multiplier,
        'confidence': confidence
    }
```

### Example

**Input:** "Build a deck"

**Historical Data:**
- 85 deck permits found
- Valuations: [$150, $200, $250, ..., $800]

**Calculations:**
- 10th percentile: $150
- 90th percentile: $600
- Median: $300
- Sample size: 85 → Confidence: 85%

**Output:**
```python
{
    'min': 150,
    'max': 600,
    'average': 300,
    'confidence': 85
}
```

**Formatted for User:**
"Estimated permit cost: $150-600 (average: $300) based on 85 similar permits"

---

## 5. Timeline Calculation

### Purpose
Estimate project timeline from application to completion.

### Algorithm

```python
def estimate_timeline(permit_types: List[str], project_complexity: str) -> Dict:
    """
    Estimate timeline for permit process
    
    Returns:
    {
        'application_prep': {'min': days, 'max': days},
        'plan_review': {'min': days, 'max': days},
        'permit_issuance': {'min': days, 'max': days},
        'total': {'min': days, 'max': days}
    }
    """
    
    # Base timelines (in business days)
    BASE_TIMELINES = {
        'application_prep': (5, 10),       # User preparation time
        'plan_review': (10, 20),           # City review
        'permit_issuance': (3, 7)          # Final issuance
    }
    
    # Complexity multipliers
    COMPLEXITY_FACTORS = {
        'simple': 1.0,
        'moderate': 1.5,
        'complex': 2.0
    }
    
    # Multiple permit penalty
    permit_count_factor = 1.0 + (len(permit_types) - 1) * 0.3
    
    # Apply complexity
    complexity_factor = COMPLEXITY_FACTORS.get(project_complexity, 1.5)
    
    # Calculate adjusted timelines
    timelines = {}
    total_min = 0
    total_max = 0
    
    for phase, (base_min, base_max) in BASE_TIMELINES.items():
        adjusted_min = base_min * complexity_factor * permit_count_factor
        adjusted_max = base_max * complexity_factor * permit_count_factor
        
        timelines[phase] = {
            'min': int(adjusted_min),
            'max': int(adjusted_max)
        }
        
        total_min += adjusted_min
        total_max += adjusted_max
    
    timelines['total'] = {
        'min': int(total_min),
        'max': int(total_max),
        'weeks_min': int(total_min / 5),  # Business days to weeks
        'weeks_max': int(total_max / 5)
    }
    
    return timelines
```

### Example

**Input:**
- Permits: ['Building Permit', 'Electrical Permit']
- Complexity: 'moderate'

**Calculations:**
- Base application prep: 5-10 days
- Complexity factor: 1.5
- Multiple permits factor: 1.3
- Adjusted prep: 5 × 1.5 × 1.3 = 9.75 → 10 days

**Output:**
```python
{
    'application_prep': {'min': 10, 'max': 19},
    'plan_review': {'min': 19, 'max': 39},
    'permit_issuance': {'min': 6, 'max': 14},
    'total': {
        'min': 35,
        'max': 72,
        'weeks_min': 7,
        'weeks_max': 14
    }
}
```

**Formatted for User:**
"Estimated timeline: 7-14 weeks from application to permit issuance"

---

## 6. Neighborhood Matching

### Purpose
Match user's location query to official neighborhood names.

### Algorithm

```python
def match_neighborhood(user_input: str, neighborhoods: List[str]) -> Dict:
    """
    Match user input to official neighborhood
    
    Returns:
    {
        'match': str,
        'confidence': float,
        'alternatives': List[str]
    }
    """
    
    user_lower = user_input.lower().strip()
    
    # 1. Exact match
    for neighborhood in neighborhoods:
        if user_lower == neighborhood.lower():
            return {
                'match': neighborhood,
                'confidence': 100,
                'alternatives': []
            }
    
    # 2. Fuzzy match using Levenshtein distance
    scores = []
    for neighborhood in neighborhoods:
        distance = levenshtein_distance(user_lower, neighborhood.lower())
        max_len = max(len(user_lower), len(neighborhood))
        similarity = (1 - distance / max_len) * 100
        scores.append((neighborhood, similarity))
    
    # Sort by similarity
    scores.sort(key=lambda x: x[1], reverse=True)
    
    best_match, best_score = scores[0]
    alternatives = [n for n, s in scores[1:4] if s > 60]
    
    return {
        'match': best_match,
        'confidence': best_score,
        'alternatives': alternatives
    }

def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculate edit distance between two strings"""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]
```

### Example

**Input:** "dowtown" (typo)

**Neighborhoods:** ["Downtown", "Uptown", "Midtown", "Old Town", ...]

**Calculations:**
- Levenshtein("dowtown", "downtown") = 1 (one missing 'n')
- Similarity: (1 - 1/8) × 100 = 87.5%

**Output:**
```python
{
    'match': 'Downtown',
    'confidence': 87.5,
    'alternatives': ['Midtown', 'Old Town']
}
```

**UI Behavior:**
- If confidence > 90: Auto-select
- If 70 < confidence < 90: Show suggestion
- If confidence < 70: Show alternatives

---

## 7. Data Freshness Scoring

### Purpose
Prioritize recent data over outdated information.

### Algorithm

```python
def calculate_freshness_score(date_str: str) -> float:
    """
    Score data freshness (0-100)
    100 = today, 0 = very old
    """
    
    from datetime import datetime, timedelta
    
    try:
        data_date = datetime.strptime(date_str, '%Y-%m-%d')
        today = datetime.now()
        age_days = (today - data_date).days
        
        # Scoring curve
        if age_days <= 30:
            return 100  # Last month: perfect
        elif age_days <= 180:
            return 90 - ((age_days - 30) / 150) * 30  # 6 months: 90-60
        elif age_days <= 365:
            return 60 - ((age_days - 180) / 185) * 30  # 1 year: 60-30
        else:
            return max(30 - (age_days - 365) / 365 * 30, 0)  # Older: 30-0
            
    except:
        return 50  # Unknown date: neutral score
```

### Decay Curve

```
Score
 100 ┤                 ╭────────
  90 ┤              ╭──╯
  80 ┤            ╭─╯
  70 ┤          ╭─╯
  60 ┤        ╭─╯
  50 ┤      ╭─╯
  40 ┤    ╭─╯
  30 ┤  ╭─╯
  20 ┤╭─╯
  10 ┼╯
   0 ┴────────────────────────────────> Days
     0   30  90  180      365      730
```

---

## 8. Composite Scoring Example

### Complete Workflow: "Build a deck" Query

```python
# Step 1: Search for relevant permits
permits = get_all_permits()

# Step 2: Score each permit
scored_permits = []
for permit in permits:
    relevance = score_permit_relevance("build a deck", permit)
    freshness = calculate_freshness_score(permit['date_approval_issue'])
    
    # Composite score (70% relevance, 30% freshness)
    composite = relevance * 0.7 + freshness * 0.3
    
    scored_permits.append((permit, composite))

# Step 3: Sort and select top 10
scored_permits.sort(key=lambda x: x[1], reverse=True)
top_permits = scored_permits[:10]

# Step 4: Build context with top permits
context = build_context("build a deck", top_permits)

# Step 5: Get AI response
response = claude.generate(context)

# Step 6: Validate response quality
quality = calculate_response_quality(response, "build a deck")

if quality < 60:
    # Regenerate with adjusted prompt
    response = claude.generate(context, temperature=0.7)
```

---

## Summary

The San Diego Permit FAQ Bot uses multiple scoring algorithms:

1. **Permit Relevance** - Ranks permits by query match (40% type, 30% title, 20% description, 10% recency)
2. **Context Prioritization** - Manages token budget (query > permits > stats > code)
3. **Response Quality** - Validates AI output (length, structure, specificity, CTA)
4. **Cost Estimation** - Statistical analysis of historical data (10th-90th percentile)
5. **Timeline Calculation** - Complexity-adjusted estimates (base × complexity × permit count)
6. **Neighborhood Matching** - Fuzzy string matching (Levenshtein distance)
7. **Data Freshness** - Time-decay scoring (100 for recent → 0 for old)

These algorithms work together to ensure accurate, relevant, and timely responses.

---

**Algorithm Version:** 2.0.0  
**Last Updated:** March 2026  
**Author:** Kedar Kulkarni