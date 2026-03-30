# Technical Documentation
## San Diego Permit FAQ Bot

**Version:** 2.0.0  
**Author:** Kedar Kulkarni  
**Last Updated:** March 2026

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Setup & Installation](#setup--installation)
5. [Configuration](#configuration)
6. [Data Management](#data-management)
7. [AI Integration](#ai-integration)
8. [Deployment](#deployment)
9. [Performance Optimization](#performance-optimization)
10. [Security](#security)
11. [Monitoring & Logging](#monitoring--logging)
12. [Troubleshooting](#troubleshooting)

---

## 1. System Overview

### 1.1 Purpose
AI-powered chatbot for navigating San Diego's municipal permit system using real government data and Claude Sonnet 4.6.

### 1.2 Key Components
- **Frontend**: Streamlit web application
- **AI Engine**: Claude Sonnet 4.6 (Anthropic)
- **Data Layer**: Pandas + CSV files / Remote URLs
- **Deployment**: Streamlit Cloud

### 1.3 System Requirements

**Development:**
- Python 3.8+
- 8GB RAM minimum
- Internet connection
- 2GB disk space (with local data)

**Production:**
- Streamlit Cloud (free tier)
- Anthropic API access
- Internet connection

---

## 2. Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────┐
│           User Interface Layer              │
│         (Streamlit Web App)                 │
│  - Chat Interface                           │
│  - Checklist Generator                      │
│  - Meeting Summarizer                       │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│         Application Layer (app.py)          │
│  - UI Logic                                 │
│  - State Management                         │
│  - User Interaction Handling                │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│          AI Layer (bot.py)                  │
│  - Claude API Integration                   │
│  - Prompt Engineering                       │
│  - Response Generation                      │
│  - Context Management                       │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│      Data Layer (data_loader.py)            │
│  - CSV File Loading                         │
│  - Remote URL Downloads                     │
│  - Data Validation                          │
│  - Caching                                  │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│          Data Sources                       │
│  - Local CSV Files (Development)            │
│  - San Diego Open Data Portal (Production)  │
│  - Municipal Code PDFs                      │
└─────────────────────────────────────────────┘
```

### 2.2 Component Interactions

**Request Flow:**
1. User enters question → Streamlit captures input
2. app.py validates and routes request
3. bot.py adds context from data_loader
4. Claude API processes request
5. Response flows back through layers
6. Streamlit renders formatted response

---

## 3. Technology Stack

### 3.1 Core Technologies

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Language | Python | 3.8+ | Core development |
| Web Framework | Streamlit | 1.30+ | UI/UX |
| AI Model | Claude Sonnet 4.6 | Latest | NLP & Generation |
| Data Processing | Pandas | 2.0+ | Data manipulation |
| PDF Processing | PyPDF2 | 3.0+ | Document parsing |
| Environment | python-dotenv | 1.0+ | Config management |

### 3.2 External Services

- **Anthropic API**: Claude Sonnet 4.6 access
- **San Diego Open Data Portal**: Government data source
- **Streamlit Cloud**: Hosting platform

### 3.3 Development Tools

- **Git**: Version control
- **VS Code**: IDE
- **Python venv**: Environment isolation
- **pip**: Package management

---

## 4. Setup & Installation

### 4.1 Prerequisites

```bash
# Check Python version
python --version  # Should be 3.8+

# Check pip
pip --version
```

### 4.2 Clone Repository

```bash
git clone https://github.com/kulkarnikk07/sd-faq-bot.git
cd sd-faq-bot
```

### 4.3 Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 4.4 Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
anthropic>=0.18.0
python-dotenv>=1.0.0
pandas>=2.0.0
numpy>=1.24.0
PyPDF2>=3.0.0
streamlit>=1.30.0
```

### 4.5 Configure Environment

Create `.env` file:
```env
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

### 4.6 Optional: Download Local Data

For faster development, download CSV files from [data.sandiego.gov](https://data.sandiego.gov):

```
data/
├── cmty_plan_datasd.csv
├── council_districts_datasd.csv
├── pd_neighborhoods_datasd.csv
├── permits_set2_active_datasd.csv
├── permits_set2_closed_datasd.csv
├── permits_project_tags_datasd.csv
└── zoning_datasd.csv
```

### 4.7 Run Application

```bash
streamlit run app.py
```

Open browser to `http://localhost:8501`

---

## 5. Configuration

### 5.1 Environment Variables

**Local Development (.env):**
```env
ANTHROPIC_API_KEY=sk-ant-api03-...
PORT=8501
DEBUG=True
```

**Streamlit Cloud (Secrets):**
```toml
ANTHROPIC_API_KEY = "sk-ant-api03-..."
```

### 5.2 Data Configuration

**data_loader.py - Line 21-28:**
```python
DATA_URLS = {
    'permits_active': 'https://seshat.datasd.org/dsd/dsd_approvals_set2_active.csv',
    'permits_closed': 'https://seshat.datasd.org/dsd/dsd_approvals_set2_closed.csv',
    'communities': 'https://seshat.datasd.org/sde/cmty_plan_datasd.csv',
    # ... other URLs
}
```

### 5.3 AI Model Configuration

**bot.py - Line 36:**
```python
self.model = "claude-sonnet-4-6"  # Model identifier
```

**Response Length:**
```python
max_tokens = 2000  # Default response length
```

---

## 6. Data Management

### 6.1 Data Sources

**Primary Sources:**
1. San Diego Open Data Portal (remote)
2. Local CSV files (development)

**Data Types:**
- Permits: 390,000+ records
- Communities: 61 neighborhoods
- Council Districts: 9 districts
- Zoning: 3,600+ designations

### 6.2 Smart Data Loading

**Environment Detection:**
```python
def _check_local_data(self) -> bool:
    """Auto-detect if local files exist"""
    if not self.data_dir.exists():
        return False
    csv_files = list(self.data_dir.rglob("*.csv"))
    return len(csv_files) > 0
```

**Loading Strategy:**
1. Check for local files
2. If found → use local
3. If not found → download from URL
4. Cache in memory for session

### 6.3 Data Validation

```python
def _load_csv(self, local_path, url_key, description):
    try:
        # Load data
        df = pd.read_csv(source, low_memory=False)
        
        # Validate
        if df.empty:
            print(f"Warning: {description} is empty")
            return None
        
        return df
    except Exception as e:
        print(f"Error loading {description}: {e}")
        return None
```

### 6.4 Data Updates

**Manual Update:**
```bash
# Download latest data from portal
# Replace files in data/ folder
# Restart application
```

**Automatic Update (Production):**
- Downloads fresh data on each deployment
- No manual intervention needed

---

## 7. AI Integration

### 7.1 Claude API Setup

**Authentication:**
```python
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
```

**Model Selection:**
```python
model = "claude-sonnet-4-6"  # Latest Sonnet
```

### 7.2 Prompt Engineering

**System Prompt Structure:**
```python
system_prompt = f"""
You are a helpful assistant for San Diego municipal permits.

Context: {knowledge_base_context}

Guidelines:
- Be conversational and friendly
- Cite specific sources
- Prioritize accuracy
- Suggest contacting Development Services for complex cases
"""
```

**User Prompt:**
```python
user_prompt = f"{question}\n\nRelevant examples:\n{permit_examples}"
```

### 7.3 Response Generation

```python
response = client.messages.create(
    model=self.model,
    max_tokens=2000,
    system=system_prompt,
    messages=[
        {"role": "user", "content": user_prompt}
    ]
)

answer = response.content[0].text
```

### 7.4 Context Management

**Knowledge Base:**
- Municipal code text (from PDFs)
- Permit statistics (from CSVs)
- Neighborhood information
- Recent permit examples

**Context Limits:**
- Max context: ~200,000 tokens
- Truncated if exceeds limit
- Prioritizes recent/relevant data

### 7.5 Error Handling

```python
try:
    response = bot.ask(question)
except Exception as e:
    return f"Error: {str(e)}\nPlease check API key and try again."
```

---

## 8. Deployment

### 8.1 Streamlit Cloud Deployment

**Prerequisites:**
- GitHub repository
- Streamlit Cloud account
- Anthropic API key

**Steps:**

1. **Push to GitHub:**
```bash
git add .
git commit -m "Deploy to Streamlit Cloud"
git push origin main
```

2. **Deploy on Streamlit:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select repository: `kulkarnikk07/sd-faq-bot`
   - Main file: `app.py`
   - Branch: `main`

3. **Configure Secrets:**
   - Click "Advanced settings"
   - Add secrets:
   ```toml
   ANTHROPIC_API_KEY = "your-key"
   ```

4. **Deploy:**
   - Click "Deploy"
   - Wait 2-3 minutes
   - App goes live

### 8.2 Custom Domain (Optional)

```bash
# In Streamlit Cloud settings
# Add custom domain: yourdomain.com
# Update DNS records as instructed
```

### 8.3 Deployment Checklist

- [ ] All code pushed to GitHub
- [ ] .gitignore excludes secrets
- [ ] API key in Streamlit secrets
- [ ] Data URLs configured
- [ ] README.md updated
- [ ] Test deployment works

---

## 9. Performance Optimization

### 9.1 Data Caching

**Streamlit Caching:**
```python
@st.cache_resource
def initialize_bot():
    """Cache bot initialization"""
    data_loader = load_data()
    bot = create_bot(data_loader)
    return bot, data_loader
```

**Benefits:**
- Loads data once per session
- Reuses bot instance
- Faster subsequent requests

### 9.2 API Call Optimization

**Reduce Context Size:**
```python
# Don't send all 390K permits
# Send only relevant subset
relevant_permits = search_permits(keywords, limit=10)
context = build_context(relevant_permits)
```

**Estimated Savings:** 50-70% on input tokens

### 9.3 Response Streaming

```python
# Future enhancement
response = client.messages.stream(
    model=self.model,
    max_tokens=2000,
    messages=[...]
)

for chunk in response:
    yield chunk.text
```

### 9.4 Database Considerations

**Current:** In-memory (Pandas DataFrames)

**Future:** PostgreSQL/SQLite for:
- Faster queries
- Persistent caching
- Advanced filtering

### 9.5 Performance Metrics

**Current Performance:**
- Page load: <3 seconds
- Data loading: 5-30 seconds (first time)
- API response: 2-5 seconds
- Total query time: 3-8 seconds

**Target Performance:**
- Page load: <2 seconds
- Data loading: <10 seconds
- API response: 2-4 seconds
- Total query time: <5 seconds

---

## 10. Security

### 10.1 API Key Management

**Never:**
- ❌ Commit API keys to GitHub
- ❌ Hardcode in source code
- ❌ Share in public forums

**Always:**
- ✅ Use environment variables
- ✅ Store in .env (local)
- ✅ Use Streamlit secrets (cloud)
- ✅ Add to .gitignore

### 10.2 Input Validation

```python
def validate_input(user_input: str) -> bool:
    """Validate user input"""
    if not user_input or len(user_input.strip()) == 0:
        return False
    if len(user_input) > 5000:  # Reasonable limit
        return False
    return True
```

### 10.3 Rate Limiting

**Recommended Implementation:**
```python
from functools import wraps
import time

def rate_limit(max_calls=10, period=60):
    """Limit API calls per user"""
    def decorator(func):
        calls = []
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [c for c in calls if c > now - period]
            if len(calls) >= max_calls:
                raise Exception("Rate limit exceeded")
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

### 10.4 Data Privacy

- No personal user data collected
- No conversation history stored
- Session-only memory
- GDPR compliant

### 10.5 HTTPS

- Streamlit Cloud uses HTTPS by default
- All API calls encrypted
- Secure data transmission

---

## 11. Monitoring & Logging

### 11.1 Application Logs

**Console Logging:**
```python
print(f"Loading San Diego data from {mode}...")
print(f"✓ Loaded {len(df)} rows")
```

**Error Logging:**
```python
try:
    response = bot.ask(question)
except Exception as e:
    print(f"Error: {e}")
    st.error(f"❌ Error: {str(e)}")
```

### 11.2 Performance Monitoring

**Track Key Metrics:**
- API response times
- Data loading times
- Error rates
- User sessions

**Implementation:**
```python
import time

start = time.time()
response = bot.ask(question)
duration = time.time() - start

print(f"Response time: {duration:.2f}s")
```

### 11.3 Usage Analytics

**Recommended Tools:**
- Streamlit Analytics (built-in)
- Google Analytics
- Plausible Analytics

**Key Metrics:**
- Daily active users
- Questions per session
- Most common queries
- Feature usage (Chat vs Checklist vs Summary)

### 11.4 Error Tracking

**Recommended:**
- Sentry for error tracking
- Custom error dashboard
- Email alerts for critical errors

---

## 12. Troubleshooting

### 12.1 Common Issues

**Issue:** "ANTHROPIC_API_KEY not found"

**Solution:**
```bash
# Check .env file exists
cat .env

# Verify key is set
echo $ANTHROPIC_API_KEY

# For Streamlit Cloud: check secrets
```

---

**Issue:** "No data loaded / Empty dropdown"

**Solution:**
```bash
# Test data loader
python data_loader.py

# Check file structure
ls -la data/

# Verify internet connection (for URL loading)
```

---

**Issue:** "Rate limit exceeded"

**Solution:**
- Wait and retry
- Check Anthropic dashboard for limits
- Implement caching
- Upgrade API plan

---

**Issue:** "Slow response times"

**Solution:**
- Reduce context size
- Implement caching
- Optimize prompts
- Use faster model (Haiku)

---

**Issue:** "Deployment fails on Streamlit Cloud"

**Solution:**
```bash
# Check requirements.txt
pip freeze > requirements.txt

# Verify no large files in repo
git rm large_file.csv

# Check secrets are set
# Verify API key is valid
```

---

### 12.2 Debug Mode

**Enable Debug Output:**
```python
# In app.py
DEBUG = True

if DEBUG:
    st.write("Debug info:", data_summary)
```

**Check Logs:**
```bash
# Local
# Check terminal output

# Streamlit Cloud
# View logs in dashboard
```

### 12.3 Testing

**Unit Tests:**
```python
# test_data_loader.py
def test_load_data():
    loader = load_data()
    assert loader.permits_data is not None
    assert len(loader.permits_data['active']) > 0

# Run tests
pytest test_data_loader.py
```

**Integration Tests:**
```python
# test_bot.py
def test_ask_question():
    loader = load_data()
    bot = create_bot(loader)
    response = bot.ask("Test question")
    assert len(response) > 0
    assert "error" not in response.lower()
```

---

## 13. Maintenance

### 13.1 Regular Tasks

**Weekly:**
- Monitor error rates
- Check API usage/costs
- Review user feedback

**Monthly:**
- Update dependencies
- Review data freshness
- Performance optimization
- Security audit

**Quarterly:**
- Major feature updates
- Data source verification
- User survey
- Documentation updates

### 13.2 Dependency Updates

```bash
# Check outdated packages
pip list --outdated

# Update specific package
pip install --upgrade streamlit

# Update all
pip install --upgrade -r requirements.txt

# Test thoroughly after updates
```

### 13.3 Data Refresh

**Manual:**
```bash
# Download latest CSVs from data.sandiego.gov
# Replace files in data/
# Test locally
# Deploy
```

**Automatic (Production):**
- Happens on each deployment
- No action needed

---

## 14. Best Practices

### 14.1 Code Quality

- Follow PEP 8 style guide
- Use type hints
- Write docstrings
- Keep functions focused
- DRY principle

### 14.2 Git Workflow

```bash
# Feature branch
git checkout -b feature/new-feature

# Commit regularly
git commit -m "Add: specific feature"

# Push and PR
git push origin feature/new-feature
```

### 14.3 Documentation

- Update README for user-facing changes
- Update this doc for technical changes
- Comment complex logic
- Maintain changelog

---

## Appendix

### A. File Structure

```
sd-faq-bot/
├── app.py              # Main Streamlit app
├── bot.py              # AI integration
├── data_loader.py      # Data management
├── requirements.txt    # Dependencies
├── .env               # Local config (git ignored)
├── .gitignore         # Git exclusions
├── README.md          # User documentation
├── docs/              # Technical docs
│   ├── PRD.md
│   ├── API_DOCUMENTATION.md
│   └── TECHNICAL_DOCUMENTATION.md
└── data/              # Local data (git ignored)
    └── *.csv
```

### B. Key Files

**app.py**: 400+ lines, UI logic  
**bot.py**: 200+ lines, AI integration  
**data_loader.py**: 400+ lines, data management  

### C. External Resources

- [Streamlit Docs](https://docs.streamlit.io)
- [Anthropic Docs](https://docs.anthropic.com)
- [San Diego Open Data](https://data.sandiego.gov)
- [Pandas Docs](https://pandas.pydata.org)

---

**Document Version:** 2.0.0  
**Last Updated:** March 2026  
**Maintained By:** Kedar Kulkarni