# API Documentation
## San Diego Permit FAQ Bot

**Version:** 2.0.0  
**Base URL:** `http://localhost:8501` (local) or `https://your-app.streamlit.app` (production)  
**Protocol:** HTTP/HTTPS  
**Authentication:** None (public endpoints)

---

## Table of Contents

1. [Overview](#overview)
2. [Data Loader API](#data-loader-api)
3. [Bot API](#bot-api)
4. [Internal Methods](#internal-methods)
5. [Error Handling](#error-handling)
6. [Rate Limiting](#rate-limiting)
7. [Examples](#examples)

---

## Overview

The San Diego FAQ Bot exposes several internal APIs through its Python modules. While there are no REST endpoints (it's a Streamlit app), the core functionality is accessible through Python function calls.

### Architecture
```
User Interface (Streamlit)
        ↓
    app.py (UI Layer)
        ↓
    bot.py (AI Layer)
        ↓
data_loader.py (Data Layer)
        ↓
External Sources (CSV files / URLs)
```

---

## Data Loader API

### Module: `data_loader.py`

The Data Loader handles all data ingestion from local files or remote URLs.

---

### Class: `SanDiegoDataLoader`

Main class for loading and managing San Diego permit data.

#### Constructor

```python
SanDiegoDataLoader(data_dir: str = "data")
```

**Parameters:**
- `data_dir` (str, optional): Path to data directory. Default: `"data"`

**Returns:**
- SanDiegoDataLoader instance

**Example:**
```python
from data_loader import SanDiegoDataLoader

loader = SanDiegoDataLoader(data_dir="data")
```

---

#### Method: `load_all_data()`

Loads all available data sources (permits, neighborhoods, zoning, PDFs).

```python
loader.load_all_data() -> SanDiegoDataLoader
```

**Parameters:** None

**Returns:**
- Self (for method chaining)

**Side Effects:**
- Populates `permits_data`, `neighborhoods_data`, `zoning_data`, `pdf_content`
- Prints loading status to console

**Example:**
```python
loader = SanDiegoDataLoader()
loader.load_all_data()
```

**Console Output:**
```
Loading San Diego data from local files...
Loading active permits from local file: data/permits_set2_active_datasd.csv
  ✓ Loaded 257692 rows
...
✅ All data loaded successfully!
```

---

#### Method: `get_permit_statistics()`

Returns summary statistics about loaded permits.

```python
loader.get_permit_statistics() -> Dict
```

**Parameters:** None

**Returns:**
```python
{
    "active_count": int,
    "closed_count": int,
    "active_by_type": Dict[str, int],  # Optional
    "closed_by_type": Dict[str, int]   # Optional
}
```

**Example:**
```python
stats = loader.get_permit_statistics()
print(f"Active permits: {stats['active_count']}")
# Output: Active permits: 257692
```

---

#### Method: `search_permits()`

Search permits by keyword across multiple columns.

```python
loader.search_permits(query: str, limit: int = 10) -> List[Dict]
```

**Parameters:**
- `query` (str): Search keyword
- `limit` (int, optional): Maximum results. Default: 10

**Returns:**
- List of permit dictionaries matching the query

**Search Columns:**
- `approval_type`
- `project_title`
- `work_description`

**Example:**
```python
results = loader.search_permits("fence", limit=5)
for permit in results:
    print(permit['approval_type'], permit['project_title'])
```

---

#### Method: `get_community_info()`

Get information about a specific San Diego community.

```python
loader.get_community_info(community_name: str) -> Optional[Dict]
```

**Parameters:**
- `community_name` (str): Name of community (case-insensitive)

**Returns:**
- Dictionary with community info, or None if not found

**Example:**
```python
info = loader.get_community_info("Downtown")
if info:
    print(f"Community: {info['cpname']}")
    print(f"Acreage: {info['acreage']}")
```

---

#### Method: `get_knowledge_base_text()`

Combines all loaded data into a single text context for AI processing.

```python
loader.get_knowledge_base_text() -> str
```

**Parameters:** None

**Returns:**
- String containing all text content (PDFs + data summaries)

**Example:**
```python
context = loader.get_knowledge_base_text()
print(f"Context length: {len(context)} characters")
```

---

#### Method: `get_data_summary()`

Returns detailed summary of all loaded data.

```python
loader.get_data_summary() -> Dict
```

**Returns:**
```python
{
    "permits": {
        "active": {"rows": int, "columns": List[str]},
        "closed": {"rows": int, "columns": List[str]},
        ...
    },
    "neighborhoods": {
        "communities": {"rows": int, "columns": List[str]},
        ...
    },
    "zoning": {...},
    "documents": {...},
    "data_source": "local files" | "remote URLs"
}
```

**Example:**
```python
summary = loader.get_data_summary()
print(f"Data source: {summary['data_source']}")
print(f"Communities: {summary['neighborhoods']['communities']['rows']}")
```

---

### Convenience Function: `load_data()`

Shortcut to create and initialize a data loader.

```python
from data_loader import load_data

loader = load_data(data_dir: str = "data") -> SanDiegoDataLoader
```

**Parameters:**
- `data_dir` (str, optional): Path to data directory

**Returns:**
- Initialized SanDiegoDataLoader instance with data loaded

**Example:**
```python
from data_loader import load_data

loader = load_data()
stats = loader.get_permit_statistics()
```

---

## Bot API

### Module: `bot.py`

The Bot handles AI interactions using Claude Sonnet 4.6.

---

### Class: `SanDiegoBot`

Main class for AI-powered question answering.

#### Constructor

```python
SanDiegoBot(data_loader, api_key: Optional[str] = None)
```

**Parameters:**
- `data_loader` (SanDiegoDataLoader): Initialized data loader instance
- `api_key` (str, optional): Anthropic API key. If None, reads from `ANTHROPIC_API_KEY` environment variable

**Raises:**
- `ValueError`: If API key not found

**Example:**
```python
from data_loader import load_data
from bot import SanDiegoBot

loader = load_data()
bot = SanDiegoBot(loader)
```

---

#### Method: `ask()`

Ask a question and get an AI-generated response.

```python
bot.ask(question: str, max_tokens: int = 2000) -> str
```

**Parameters:**
- `question` (str): User's question
- `max_tokens` (int, optional): Maximum response length. Default: 2000

**Returns:**
- String response from Claude

**Example:**
```python
response = bot.ask("What permits do I need to build a fence?")
print(response)
```

**Response Time:** Typically 2-5 seconds

---

#### Method: `generate_permit_checklist()`

Generate a customized permit checklist for a project.

```python
bot.generate_permit_checklist(project_description: str) -> str
```

**Parameters:**
- `project_description` (str): One-line project description

**Returns:**
- Formatted checklist string with:
  - Required permits
  - Estimated timeline
  - Approximate costs
  - Considerations
  - Next steps

**Example:**
```python
checklist = bot.generate_permit_checklist(
    "Build a 12x20 deck with electrical lighting"
)
print(checklist)
```

---

#### Method: `summarize_for_neighborhood()`

Summarize content for a specific neighborhood.

```python
bot.summarize_for_neighborhood(
    content: str, 
    neighborhood: str
) -> str
```

**Parameters:**
- `content` (str): Meeting transcript or content to summarize
- `neighborhood` (str): San Diego neighborhood name

**Returns:**
- Neighborhood-specific summary with:
  - Key decisions affecting the neighborhood
  - Upcoming projects
  - Action items
  - Important dates

**Example:**
```python
transcript = "Council meeting transcript..."
summary = bot.summarize_for_neighborhood(transcript, "Downtown")
print(summary)
```

---

#### Method: `chat()`

Continue a multi-turn conversation with context.

```python
bot.chat(
    conversation_history: List[Dict[str, str]], 
    new_message: str
) -> str
```

**Parameters:**
- `conversation_history` (List[Dict]): Previous messages
- `new_message` (str): New user message

**Conversation History Format:**
```python
[
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi! How can I help?"},
    {"role": "user", "content": "What permits..."}
]
```

**Returns:**
- String response from Claude

**Example:**
```python
history = [
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello! How can I help?"}
]

response = bot.chat(history, "What permits do I need?")
```

---

### Convenience Function: `create_bot()`

Shortcut to create a bot instance.

```python
from bot import create_bot

bot = create_bot(data_loader, api_key: Optional[str] = None) -> SanDiegoBot
```

**Example:**
```python
from data_loader import load_data
from bot import create_bot

loader = load_data()
bot = create_bot(loader)
```

---

## Internal Methods

### Private Methods (Not for External Use)

#### `SanDiegoDataLoader._check_local_data()`
Checks if local CSV files exist.

#### `SanDiegoDataLoader._load_csv()`
Internal method to load CSV from local file or URL.

#### `SanDiegoBot._build_system_prompt()`
Constructs the system prompt with context.

#### `SanDiegoBot._get_relevant_permit_examples()`
Finds relevant permit examples for context.

---

## Error Handling

### Common Errors

#### API Key Not Found
```python
ValueError: Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable or pass api_key parameter.
```

**Solution:**
```python
# Option 1: Environment variable
import os
os.environ['ANTHROPIC_API_KEY'] = 'your-key'

# Option 2: Pass directly
bot = SanDiegoBot(loader, api_key='your-key')
```

---

#### Data Loading Failure
```python
# Gracefully handled - prints warning and continues
⚠️  Permits directory not found, skipping...
```

**Behavior:** App continues with available data

---

#### Claude API Error
```python
"Error: [error message]
Please check your API key and try again."
```

**Common Causes:**
- Invalid API key
- Rate limit exceeded
- Network timeout
- Claude API downtime

---

## Rate Limiting

### Anthropic API Limits

**Claude Sonnet 4.6:**
- Requests: Varies by account tier
- Tokens: Based on usage plan

**Best Practices:**
- Implement caching for common questions
- Add user-side rate limiting
- Monitor API usage
- Use prompt optimization

### Example Rate Limiting

```python
import time
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_ask(question: str) -> str:
    """Cache responses for identical questions"""
    return bot.ask(question)

# Use cached version
response = cached_ask("What permits for fence?")
```

---

## Examples

### Example 1: Complete Workflow

```python
from data_loader import load_data
from bot import create_bot

# Initialize
loader = load_data()
bot = create_bot(loader)

# Get data summary
summary = loader.get_data_summary()
print(f"Loaded {summary['permits']['active']['rows']} permits")

# Ask a question
question = "What permits do I need to build a storage shed?"
response = bot.ask(question)
print(response)

# Generate checklist
project = "Remodel kitchen with new electrical"
checklist = bot.generate_permit_checklist(project)
print(checklist)

# Search permits
results = loader.search_permits("electrical", limit=5)
for permit in results:
    print(permit['approval_type'])
```

---

### Example 2: Multi-Turn Conversation

```python
from data_loader import load_data
from bot import create_bot

loader = load_data()
bot = create_bot(loader)

# Initialize conversation
history = []

# First question
question1 = "What permits do I need for a fence?"
response1 = bot.chat(history, question1)
history.append({"role": "user", "content": question1})
history.append({"role": "assistant", "content": response1})

# Follow-up question
question2 = "How much will that cost?"
response2 = bot.chat(history, question2)
print(response2)  # Context-aware response
```

---

### Example 3: Neighborhood Summary

```python
from data_loader import load_data
from bot import create_bot

loader = load_data()
bot = create_bot(loader)

# Get community info
community = loader.get_community_info("Downtown")
print(f"Community: {community['cpname']}")

# Summarize meeting
transcript = """
Council approved new housing development in Downtown.
La Jolla beach access improvements discussed.
Barrio Logan community center funding approved.
"""

summary = bot.summarize_for_neighborhood(transcript, "Downtown")
print(summary)
# Output focuses only on Downtown items
```

---

### Example 4: Error Handling

```python
from data_loader import load_data
from bot import create_bot

try:
    loader = load_data()
    bot = create_bot(loader)
    
    response = bot.ask("What permits for fence?")
    print(response)
    
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Data Schemas

### Permit Record Schema

```python
{
    "PROJECT_ID": str,
    "APPROVAL_TYPE": str,
    "PROJECT_TITLE": str,
    "APPROVAL_SCOPE": str,
    "ADDRESS_JOB": str,
    "DATE_APPROVAL_ISSUE": str,
    "APPROVAL_VALUATION": float,
    ...
}
```

### Community Record Schema

```python
{
    "objectid": int,
    "cpcode": str,
    "cpname": str,
    "acreage": float
}
```

---

## Environment Variables

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-api03-...

# Optional
PORT=8501
DEBUG=True
```

---

## Dependencies

```python
# Core
anthropic>=0.18.0
python-dotenv>=1.0.0

# Data
pandas>=2.0.0
PyPDF2>=3.0.0

# UI
streamlit>=1.30.0
```

---

## Version History

### v2.0.0 (Current)
- Added URL-based data loading
- Upgraded to Claude Sonnet 4.6
- Improved error handling
- Enhanced documentation

### v1.0.0
- Initial release
- Basic Q&A functionality
- Local data loading only

---

**API Documentation Version:** 2.0.0  
**Last Updated:** March 2026  
**Maintained By:** Kedar Kulkarni