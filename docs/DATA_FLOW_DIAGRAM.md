# Data Flow Diagram
## San Diego Permit FAQ Bot

**Version:** 2.0.0  
**Date:** March 2026

---

## Overview

This document describes how data flows through the San Diego Permit FAQ Bot system, from user input to final response.

---

## 1. Complete System Data Flow

```
┌──────────────────────────────────────────────────────────────┐
│                    USER INPUT                                │
│  • Question                                                  │
│  • Project description                                       │
│  • Meeting transcript                                        │
└─────────────────────┬────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│               INPUT VALIDATION                               │
│  • Check empty input                                         │
│  • Verify length (< 5000 chars)                              │
│  • Sanitize special characters                               │
└─────────────────────┬────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│              ROUTING LAYER (app.py)                          │
│  • Tab 1: Question → ask()                                   │
│  • Tab 2: Project → generate_permit_checklist()              │
│  • Tab 3: Transcript → summarize_for_neighborhood()          │
└─────────────────────┬────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│           CONTEXT PREPARATION (bot.py)                       │
│                                                              │
│  Step 1: Get Knowledge Base                                 │
│    data_loader.get_knowledge_base_text()                    │
│    → 390K+ permit records                                   │
│    → Municipal code (PDFs)                                  │
│    → Neighborhood data                                      │
│                                                              │
│  Step 2: Get Relevant Examples                              │
│    data_loader.search_permits(keywords)                     │
│    → Top 10 matching permits                                │
│                                                              │
│  Step 3: Build System Prompt                                │
│    "You are a San Diego permit assistant..."                │
│    + Knowledge base context                                 │
│    + Guidelines and constraints                             │
│                                                              │
│  Step 4: Format User Message                                │
│    User input + relevant examples                           │
└─────────────────────┬────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│            ANTHROPIC API CALL                                │
│                                                              │
│  Request:                                                    │
│  {                                                           │
│    "model": "claude-sonnet-4-6",                             │
│    "max_tokens": 2000,                                       │
│    "system": [system_prompt],                                │
│    "messages": [                                             │
│      {"role": "user", "content": user_message}               │
│    ]                                                         │
│  }                                                           │
│                                                              │
│  Processing Time: 2-5 seconds                                │
└─────────────────────┬────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│            RESPONSE PROCESSING                               │
│  • Extract text from response                                │
│  • Format markdown                                           │
│  • Add citations (if any)                                    │
│  • Handle errors                                             │
└─────────────────────┬────────────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────────────┐
│              UI RENDERING                                    │
│  • Display formatted response                                │
│  • Add download button (if applicable)                       │
│  • Update conversation history                               │
│  • Show success message                                      │
└──────────────────────────────────────────────────────────────┘
```

---

## 2. Data Loading Flow

### Startup Data Flow

```
App Start
    │
    ▼
┌────────────────────────────┐
│  Initialize Data Loader    │
│  SanDiegoDataLoader()      │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│  Check Environment         │
│  _check_local_data()       │
└────────────┬───────────────┘
             │
      ┌──────┴───────┐
      │              │
      ▼              ▼
  YES: Local    NO: Remote
      │              │
      ▼              ▼
┌──────────┐   ┌──────────┐
│ Load     │   │ Download │
│ from     │   │ from     │
│ data/    │   │ URLs     │
└────┬─────┘   └────┬─────┘
     │              │
     └──────┬───────┘
            │
            ▼
┌────────────────────────────┐
│  Load All Data Sources     │
│  • load_permits()          │
│  • load_neighborhoods()    │
│  • load_zoning()           │
│  • load_pdf_documents()    │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│  Data Validation           │
│  • Check for empty dfs     │
│  • Verify column names     │
│  • Log statistics          │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│  Cache in Memory           │
│  • permits_data            │
│  • neighborhoods_data      │
│  • zoning_data             │
│  • pdf_content             │
└────────────┬───────────────┘
             │
             ▼
        Ready for Use
```

### Data Source Details

```
LOCAL ENVIRONMENT:
data/cmty_plan_datasd.csv
    │
    ├─→ Read with Pandas
    ├─→ Parse CSV
    ├─→ Validate columns
    ├─→ Store in DataFrame
    └─→ Cache in memory

CLOUD ENVIRONMENT:
https://seshat.datasd.org/sde/cmty_plan_datasd.csv
    │
    ├─→ HTTP GET request
    ├─→ Download CSV
    ├─→ Parse with Pandas
    ├─→ Validate columns
    ├─→ Store in DataFrame
    └─→ Cache in memory
```

---

## 3. Feature-Specific Data Flows

### Feature 1: Ask Questions (Q&A)

```
User Question: "What permits for a fence?"
    │
    ▼
┌─────────────────────────────┐
│  app.py: Capture input      │
│  st.chat_input()            │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  bot.py: ask(question)      │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Get relevant permits       │
│  search_permits("fence")    │
│  → Returns 10 examples      │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Build context              │
│  "User asks: [question]     │
│   Relevant permits:         │
│   1. Fence permit #123...   │
│   2. Fence permit #456..."  │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Call Claude API            │
│  → Processing 2-5 sec       │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Response:                  │
│  "For a fence in San Diego, │
│  you typically need:        │
│  1. Building permit if..."  │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Display in chat UI         │
│  st.chat_message("ai")      │
└─────────────────────────────┘
```

**Data Touched:**
- Input: User question (text)
- Processing: 390K+ permits, Municipal code
- Output: AI-generated response (text)

---

### Feature 2: Permit Checklist Generator

```
User Input: "Build a 12x20 deck"
    │
    ▼
┌──────────────────────────────────┐
│  app.py: Tab 2 input             │
│  st.text_area()                  │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  Validate description            │
│  • Not empty?                    │
│  • Reasonable length?            │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  bot.py:                         │
│  generate_permit_checklist()     │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  Search similar projects         │
│  search_permits("deck")          │
│  → Returns deck permits          │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  Get permit statistics           │
│  get_permit_statistics()         │
│  → Average costs, timelines      │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  Build specialized prompt        │
│  "Generate checklist for:        │
│   Project: [description]         │
│   Similar permits: [examples]    │
│   Format: Markdown with          │
│   sections..."                   │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  Call Claude API                 │
│  → Processing 5-10 sec           │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  Checklist Response:             │
│  ## Required Permits             │
│  1. Building Permit - $300-500   │
│  2. Electrical Permit...         │
│  ## Timeline                     │
│  ...                             │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  Display formatted output        │
│  st.markdown(checklist)          │
│  + Download button               │
└──────────────────────────────────┘
```

**Data Touched:**
- Input: Project description (text)
- Processing: Permit database, Statistics
- Output: Formatted checklist (Markdown)

---

### Feature 3: Meeting Summarizer

```
User Input:
  • Neighborhood: "Downtown" (dropdown)
  • Content: [Meeting transcript] (text)
    │
    ▼
┌──────────────────────────────────┐
│  app.py: Tab 3 inputs            │
│  • st.selectbox()                │
│  • st.text_area()                │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  Load neighborhood dropdown      │
│  neighborhoods_data['communities']│
│  → 61 San Diego neighborhoods    │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  Validate inputs                 │
│  • Neighborhood selected?        │
│  • Content provided?             │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  bot.py:                         │
│  summarize_for_neighborhood()    │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  Get community info              │
│  get_community_info("Downtown")  │
│  → Community details, boundaries │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  Get related permits             │
│  search_permits(neighborhood)    │
│  → Recent permits in area        │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  Build context                   │
│  "Extract info about Downtown:   │
│   Community: [details]           │
│   Recent activity: [permits]     │
│   Content: [transcript]"         │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  Call Claude API                 │
│  → Processing 10-15 sec          │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  Summary Response:               │
│  ## Key Decisions for Downtown   │
│  - Housing project approved...   │
│  ## Upcoming Projects            │
│  - Transit improvements...       │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  Display summary                 │
│  st.success() + st.markdown()    │
│  + Download button               │
└──────────────────────────────────┘
```

**Data Touched:**
- Input: Neighborhood name + transcript
- Processing: Community data, Permits
- Output: Filtered summary (Markdown)

---

## 4. Data Transformation Pipeline

### Raw Data → Knowledge Base

```
RAW DATA SOURCES:
├── permits_set2_active_datasd.csv (257,692 rows)
├── permits_set2_closed_datasd.csv (132,550 rows)
├── cmty_plan_datasd.csv (61 rows)
├── council_districts_datasd.csv (9 rows)
├── pd_neighborhoods_datasd.csv (124 rows)
└── zoning_datasd.csv (3,677 rows)

    ↓ LOAD

PANDAS DATAFRAMES:
├── permits_data['active']: DataFrame
├── permits_data['closed']: DataFrame
├── neighborhoods_data['communities']: DataFrame
├── neighborhoods_data['council_districts']: DataFrame
├── neighborhoods_data['police_neighborhoods']: DataFrame
└── zoning_data['designations']: DataFrame

    ↓ PROCESS

STATISTICS:
├── Total permits: 390,242
├── Active count: 257,692
├── Closed count: 132,550
├── Neighborhoods: 61
├── Permit types: ~50 unique types
└── Average costs, timelines

    ↓ FORMAT

KNOWLEDGE BASE TEXT:
"""
=== MUNICIPAL CODE ===
[PDF content if available]

=== PERMIT INFORMATION ===
{
  "active_count": 257692,
  "closed_count": 132550,
  "active_by_type": {...}
}

=== COMMUNITY PLANNING DISTRICTS ===
San Diego has 61 communities:
Southeastern San Diego, Downtown, La Jolla...
"""

    ↓ USE

CLAUDE API CONTEXT:
System prompt includes knowledge base
→ Enables accurate, data-driven responses
```

---

## 5. Session State Flow

```
User Opens App
    │
    ▼
┌─────────────────────────┐
│  Streamlit Session      │
│  st.session_state       │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│  Initialize             │
│  • messages = []        │
│  • bot = None           │
│  • data_loader = None   │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│  Load Data (once)       │
│  @st.cache_resource     │
│  → Cached for session   │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│  User Interaction       │
│  • Ask question         │
│  • messages.append()    │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│  Maintain History       │
│  messages = [           │
│    {role: "user", ...}, │
│    {role: "ai", ...}    │
│  ]                      │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│  Close Tab/Browser      │
│  → Session cleared      │
│  → No data retained     │
└─────────────────────────┘
```

---

## 6. Error Data Flow

```
User Input
    │
    ▼
    Try:
    │
    ├─→ Validate input
    │   └─→ Invalid? → Show warning → End
    │
    ├─→ Call bot method
    │   │
    │   ├─→ Check API key
    │   │   └─→ Missing? → ValueError → Catch
    │   │
    │   ├─→ Call Claude API
    │   │   └─→ Network error? → Exception → Catch
    │   │
    │   └─→ Parse response
    │       └─→ Unexpected format? → Exception → Catch
    │
    Except Exception as e:
    │
    ├─→ Log error
    ├─→ Format user message
    └─→ Display error UI
        st.error(f"❌ Error: {str(e)}")
```

---

## 7. Download Data Flow

```
User Clicks "Download Checklist"
    │
    ▼
┌────────────────────────────┐
│  Content in memory         │
│  checklist_text (string)   │
└──────────┬─────────────────┘
           │
           ▼
┌────────────────────────────┐
│  Format for download       │
│  • Add header              │
│  • Ensure UTF-8 encoding   │
└──────────┬─────────────────┘
           │
           ▼
┌────────────────────────────┐
│  st.download_button()      │
│  • label: "📥 Download"    │
│  • data: checklist_text    │
│  • file_name: "*.md"       │
│  • mime_type: "text/md"    │
└──────────┬─────────────────┘
           │
           ▼
┌────────────────────────────┐
│  Browser Download          │
│  • Save to Downloads/      │
│  • User chooses location   │
└────────────────────────────┘
```

---

## 8. Caching Data Flow

```
First Request:
    Load data → Process → Cache → Use
    (Takes 5-30 seconds)

Subsequent Requests (Same Session):
    Retrieve from cache → Use
    (Instant)

New Session:
    Clear cache → Load data again
    (Takes 5-30 seconds)

@st.cache_resource:
    • Caches data_loader object
    • Caches bot object
    • Shared across all users
    • Persists until deployment update
```

---

## 9. API Token Flow

```
User Question (500 chars)
    │
    ▼
Add Context (10,000 chars)
    ├─→ Knowledge base: 8,000 chars
    ├─→ Examples: 1,500 chars
    └─→ Instructions: 500 chars
    │
    ▼
Total Input: ~10,500 chars
    → ~7,500 tokens
    │
    ▼
Claude API Processing
    │
    ▼
Response: ~1,000 chars
    → ~750 tokens
    │
    ▼
Total Tokens: ~8,250
Cost: ~$0.08 per request
```

---

## 10. Complete Request-Response Cycle

```
TIME: 0ms
User submits question
    │
TIME: 50ms
Input validation
    │
TIME: 100ms
Load cached data (instant)
    │
TIME: 200ms
Search relevant permits (Pandas query)
    │
TIME: 300ms
Build prompt (string formatting)
    │
TIME: 400ms
Send to Claude API
    │
TIME: 400-5000ms
Claude processes (2-5 seconds)
    │
TIME: 5100ms
Receive response
    │
TIME: 5150ms
Parse and format
    │
TIME: 5200ms
Display to user
    │
TOTAL: ~5.2 seconds
```

---

**Data Flow Version:** 2.0.0  
**Last Updated:** March 2026  
**Author:** Kedar Kulkarni