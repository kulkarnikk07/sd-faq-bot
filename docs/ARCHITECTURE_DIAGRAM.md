# System Architecture Diagram
## San Diego Permit FAQ Bot

**Version:** 2.0.0  
**Date:** March 2026

---

## High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER LAYER                              │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ Desktop  │  │  Tablet  │  │  Mobile  │  │  Browser │      │
│  │ Browser  │  │          │  │  Device  │  │   App    │      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
│       │              │              │              │           │
│       └──────────────┴──────────────┴──────────────┘           │
│                          │ HTTPS                                │
└──────────────────────────┼──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER                            │
│                   (Streamlit Cloud)                             │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                      app.py                                │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │ │
│  │  │   Tab 1:    │  │   Tab 2:    │  │   Tab 3:    │       │ │
│  │  │ Ask         │  │  Permit     │  │  Meeting    │       │ │
│  │  │ Questions   │  │ Checklist   │  │  Summary    │       │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘       │ │
│  │                                                            │ │
│  │  ┌───────────────────────────────────────────┐            │ │
│  │  │      UI Components & State Management     │            │ │
│  │  │  • Chat interface                         │            │ │
│  │  │  • Form inputs                            │            │ │
│  │  │  • Download buttons                       │            │ │
│  │  │  • Loading indicators                     │            │ │
│  │  │  • Error handling                         │            │ │
│  │  └───────────────────────────────────────────┘            │ │
│  └───────────────────────────────────────────────────────────┘ │
│                           │                                     │
└───────────────────────────┼─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER                             │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                      bot.py                                │ │
│  │                                                            │ │
│  │  ┌─────────────────────────────────────────────────────┐  │ │
│  │  │          SanDiegoBot Class                          │  │ │
│  │  │                                                     │  │ │
│  │  │  Methods:                                          │  │ │
│  │  │  • ask(question) → response                        │  │ │
│  │  │  • generate_permit_checklist(project)              │  │ │
│  │  │  • summarize_for_neighborhood(content, area)       │  │ │
│  │  │  • chat(history, message)                          │  │ │
│  │  │                                                     │  │ │
│  │  │  Internal:                                         │  │ │
│  │  │  • _build_system_prompt()                          │  │ │
│  │  │  • _get_relevant_examples()                        │  │ │
│  │  │  • _format_context()                               │  │ │
│  │  └─────────────────────────────────────────────────────┘  │ │
│  │                           │                                │ │
│  │                           │ Anthropic SDK                  │ │
│  │                           ▼                                │ │
│  │  ┌─────────────────────────────────────────────────────┐  │ │
│  │  │         Claude API Client                           │  │ │
│  │  │  • API key management                               │  │ │
│  │  │  • Request formatting                               │  │ │
│  │  │  • Response parsing                                 │  │ │
│  │  │  • Error handling                                   │  │ │
│  │  └─────────────────────────────────────────────────────┘  │ │
│  └───────────────────────────────────────────────────────────┘ │
│                           │                                     │
└───────────────────────────┼─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                 │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                  data_loader.py                            │ │
│  │                                                            │ │
│  │  ┌─────────────────────────────────────────────────────┐  │ │
│  │  │       SanDiegoDataLoader Class                      │  │ │
│  │  │                                                     │  │ │
│  │  │  Public Methods:                                   │  │ │
│  │  │  • load_all_data()                                 │  │ │
│  │  │  • get_permit_statistics()                         │  │ │
│  │  │  • search_permits(query)                           │  │ │
│  │  │  • get_community_info(name)                        │  │ │
│  │  │  • get_knowledge_base_text()                       │  │ │
│  │  │                                                     │  │ │
│  │  │  Internal Methods:                                 │  │ │
│  │  │  • _check_local_data()                             │  │ │
│  │  │  • _load_csv(path, url, desc)                      │  │ │
│  │  │  • load_permits()                                  │  │ │
│  │  │  • load_neighborhoods()                            │  │ │
│  │  │  • load_zoning()                                   │  │ │
│  │  └─────────────────────────────────────────────────────┘  │ │
│  │                           │                                │ │
│  │              ┌────────────┴────────────┐                   │ │
│  │              │                         │                   │ │
│  │              ▼                         ▼                   │ │
│  │  ┌─────────────────────┐  ┌─────────────────────┐         │ │
│  │  │  Environment        │  │  Data Processing    │         │ │
│  │  │  Detection          │  │  • Pandas           │         │ │
│  │  │  • Check local files│  │  • Validation       │         │ │
│  │  │  • Fall back to URLs│  │  • Transformation   │         │ │
│  │  └─────────────────────┘  └─────────────────────┘         │ │
│  └───────────────────────────────────────────────────────────┘ │
│                           │                                     │
│              ┌────────────┴────────────┐                       │
│              │                         │                       │
└──────────────┼─────────────────────────┼───────────────────────┘
               │                         │
               ▼                         ▼
┌─────────────────────────┐  ┌─────────────────────────┐
│   LOCAL ENVIRONMENT     │  │   CLOUD ENVIRONMENT     │
│                         │  │                         │
│  ┌──────────────────┐   │  │  ┌──────────────────┐   │
│  │   data/ folder   │   │  │  │  San Diego Open  │   │
│  │                  │   │  │  │  Data Portal     │   │
│  │  • CSV files     │   │  │  │                  │   │
│  │  • Fast loading  │   │  │  │  • Remote URLs   │   │
│  │  • 390K+ records │   │  │  │  • Auto download │   │
│  │                  │   │  │  │  • Always fresh  │   │
│  └──────────────────┘   │  │  └──────────────────┘   │
│                         │  │                         │
└─────────────────────────┘  └─────────────────────────┘
               │                         │
               └────────────┬────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  EXTERNAL SERVICES                              │
│                                                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐              │
│  │  Anthropic API      │  │  San Diego Open     │              │
│  │                     │  │  Data Portal        │              │
│  │  • Claude Sonnet 4.6│  │                     │              │
│  │  • NLP Processing   │  │  • Permits data     │              │
│  │  • Response Gen     │  │  • Neighborhoods    │              │
│  │  • Context handling │  │  • Zoning info      │              │
│  │                     │  │  • Council districts│              │
│  └─────────────────────┘  └─────────────────────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. User Layer
- **Desktop/Mobile Browsers**: Chrome, Firefox, Safari, Edge
- **Connection**: HTTPS encrypted
- **No Authentication**: Public access

### 2. Presentation Layer (Streamlit)
- **Framework**: Streamlit 1.30+
- **Hosting**: Streamlit Cloud (Free)
- **Features**:
  - Real-time UI updates
  - Session state management
  - Responsive design
  - Dark mode support

### 3. Application Layer (bot.py)
- **AI Integration**: Claude Sonnet 4.6
- **Functions**:
  - Question answering
  - Checklist generation
  - Meeting summarization
- **Response Time**: 2-5 seconds

### 4. Data Layer (data_loader.py)
- **Data Processing**: Pandas
- **Sources**: Dual (local + remote)
- **Caching**: In-memory
- **Data Size**: 390K+ records

### 5. External Services
- **Anthropic API**: $3/$15 per million tokens
- **San Diego Open Data**: Free, public

---

## Data Flow Patterns

### Pattern 1: Question-Answer Flow
```
User Question
    ↓
UI Capture (app.py)
    ↓
Context Loading (data_loader.py)
    ↓
Prompt Building (bot.py)
    ↓
Claude API Request
    ↓
Response Parsing
    ↓
UI Display
```

### Pattern 2: Checklist Generation Flow
```
Project Description
    ↓
Validation (app.py)
    ↓
Relevant Examples (data_loader.py)
    ↓
Checklist Prompt (bot.py)
    ↓
Claude API Request
    ↓
Formatted Checklist
    ↓
Download Option
```

### Pattern 3: Data Loading Flow
```
App Start
    ↓
Check Environment (data_loader.py)
    ↓
Local Files? ────YES──→ Load from data/
    │
    NO
    ↓
Download from URLs
    ↓
Validate & Cache
    ↓
Ready for Use
```

---

## Deployment Architecture

### Development Environment
```
Developer Machine
    ↓
Local Python Environment
    ↓
Streamlit Server (localhost:8501)
    ↓
Local CSV Files (data/)
    ↓
Fast Iteration
```

### Production Environment
```
GitHub Repository
    ↓
Streamlit Cloud
    ↓
Automatic Deployment
    ↓
Download Data from URLs
    ↓
Serve to Users (HTTPS)
```

---

## Security Architecture

### API Key Management
```
Development:
.env file → Environment Variable → bot.py

Production:
Streamlit Secrets → Environment Variable → bot.py
```

### Data Privacy
- No user data stored
- Session-only memory
- No tracking/analytics
- HTTPS encryption

---

## Scalability Considerations

### Current Capacity
- **Concurrent Users**: 100
- **Requests/Second**: 10
- **Data Refresh**: On deployment

### Scaling Options
1. **Horizontal**: Multiple Streamlit instances
2. **Caching**: Redis for data layer
3. **Database**: PostgreSQL for faster queries
4. **CDN**: For static assets

---

## Technology Stack Diagram

```
┌─────────────────────────────────────────┐
│         Frontend                        │
│  • Streamlit (Python-based UI)         │
│  • HTML/CSS (auto-generated)           │
│  • JavaScript (Streamlit components)   │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│         Backend                         │
│  • Python 3.8+                          │
│  • Anthropic SDK                        │
│  • Pandas (data manipulation)           │
│  • PyPDF2 (document parsing)            │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│         External APIs                   │
│  • Claude Sonnet 4.6 (Anthropic)        │
│  • San Diego Open Data Portal           │
└─────────────────────────────────────────┘
```

---

## File System Architecture

```
sd-faq-bot/
│
├── app.py                    # UI Layer
│   └── Streamlit components
│
├── bot.py                    # AI Layer
│   ├── SanDiegoBot class
│   └── Claude integration
│
├── data_loader.py            # Data Layer
│   ├── SanDiegoDataLoader class
│   └── Data processing
│
├── requirements.txt          # Dependencies
│
├── .env                      # Local config (git ignored)
│
├── .gitignore               # Git exclusions
│
├── README.md                # User docs
│
├── docs/                    # Documentation
│   ├── PRD.md
│   ├── API_DOCUMENTATION.md
│   ├── TECHNICAL_DOCUMENTATION.md
│   ├── USER_DOCUMENTATION.md
│   ├── ARCHITECTURE_DIAGRAM.md
│   ├── DATA_FLOW_DIAGRAM.md
│   └── SCORING_ALGORITHM.md
│
└── data/                    # Local data (git ignored)
    ├── cmty_plan_datasd.csv
    ├── council_districts_datasd.csv
    ├── pd_neighborhoods_datasd.csv
    ├── permits_set2_active_datasd.csv
    ├── permits_set2_closed_datasd.csv
    ├── permits_project_tags_datasd.csv
    └── zoning_datasd.csv
```

---

## Network Architecture

```
                 Internet
                    │
    ┌───────────────┼───────────────┐
    │               │               │
    ▼               ▼               ▼
User Device   Streamlit Cloud  Anthropic API
    │               │               │
    │               └───────────────┘
    │               Request/Response
    │                   (HTTPS)
    │
    └─── HTTPS ────→ Streamlit App
                        │
                        └─── HTTPS ────→ Data Sources
```

---

## Monitoring & Logging Architecture

```
Application Logs
    │
    ├── Console Output (Development)
    │   └── Print statements
    │
    └── Streamlit Logs (Production)
        └── Cloud dashboard

Performance Metrics
    │
    ├── Response Times
    ├── API Call Counts
    ├── Error Rates
    └── User Sessions

Recommended Addition:
    │
    ├── Sentry (Error tracking)
    ├── Google Analytics (Usage)
    └── Custom Dashboard (Metrics)
```

---

## Version Control Architecture

```
GitHub Repository (main branch)
    │
    ├── Development Branch
    │   └── Feature Branches
    │
    └── Automatic Deployment
        └── Streamlit Cloud
            └── Production App
```

---

## Cost Architecture

```
Monthly Costs:

Streamlit Cloud: $0 (Free tier)
    ↓
Anthropic API: $100-300
    • $0.06-0.18 per user session
    • Based on usage
    ↓
San Diego Data: $0 (Public)
    ↓
Total: $100-300/month (for 1,000+ users)
```

---

**Diagram Version:** 2.0.0  
**Last Updated:** March 2026  
**Author:** Kedar Kulkarni