# Product Requirements Document (PRD)
## San Diego Permit FAQ Bot

**Version:** 2.0.0  
**Date:** March 2026  
**Author:** Kedar Kulkarni  
**Status:** Production

---

## 1. Executive Summary

### 1.1 Product Overview
The San Diego Permit FAQ Bot is an AI-powered chatbot that simplifies navigation of San Diego's municipal permit system. It provides instant answers to permit-related questions, generates customized permit checklists, and summarizes council meetings by neighborhood using real data from the City of San Diego Open Data Portal.

### 1.2 Problem Statement
San Diego residents and contractors face significant challenges:
- Complex permit requirements across 390,000+ permit records
- Difficulty understanding municipal code and regulations
- Time-consuming process to identify required permits
- Lack of neighborhood-specific council meeting information
- Long wait times for Development Services support

### 1.3 Solution
An intelligent chatbot powered by Claude Sonnet 4.6 that:
- Answers permit questions in plain English
- Generates project-specific permit checklists
- Summarizes council meetings by neighborhood
- Provides instant access to real permit data

### 1.4 Success Metrics
- **User Engagement**: 70% of users complete their primary task
- **Response Accuracy**: 90%+ accuracy on permit questions
- **Time Savings**: Reduce permit research time by 80%
- **User Satisfaction**: 4.5+ star rating
- **Cost Efficiency**: <$0.20 per user session

---

## 2. Target Users

### 2.1 Primary Users
1. **Homeowners** (60%)
   - DIY home improvement projects
   - Need basic permit information
   - Limited technical knowledge

2. **Contractors** (25%)
   - Professional permit applications
   - Need detailed requirements
   - Frequent users

3. **Real Estate Developers** (10%)
   - Large-scale projects
   - Complex permit requirements
   - Multi-permit projects

4. **Community Activists** (5%)
   - Track neighborhood developments
   - Monitor council decisions
   - Advocacy work

### 2.2 User Personas

**Persona 1: DIY Dave**
- Age: 35-55
- Goal: Build a backyard deck
- Pain Point: Confused by permit requirements
- Need: Simple, step-by-step guidance

**Persona 2: Professional Pam**
- Age: 40-60
- Goal: Submit multiple permit applications weekly
- Pain Point: Time-consuming research
- Need: Quick, accurate permit checklists

**Persona 3: Activist Alice**
- Age: 30-50
- Goal: Stay informed about neighborhood developments
- Pain Point: Long council meeting transcripts
- Need: Neighborhood-specific summaries

---

## 3. Features & Requirements

### 3.1 Core Features (Must Have)

#### 3.1.1 Interactive Q&A Chat
**Priority:** P0 (Critical)

**User Story:**
> As a homeowner, I want to ask questions about permits in plain English so that I can quickly understand requirements without reading lengthy documents.

**Requirements:**
- Natural language question input
- Real-time AI responses using Claude Sonnet 4.6
- Context-aware answers based on municipal code
- Conversation history within session
- Sources data from 390,000+ permit records
- Response time: <5 seconds
- Support for follow-up questions

**Acceptance Criteria:**
- [ ] User can type questions in natural language
- [ ] System responds within 5 seconds
- [ ] Answers cite specific municipal codes when applicable
- [ ] Conversation history preserved during session
- [ ] Handles permit-related questions with 90%+ accuracy

---

#### 3.1.2 Permit Checklist Generator
**Priority:** P0 (Critical)

**User Story:**
> As a contractor, I want to describe my project and receive a complete permit checklist so that I don't miss any required permits.

**Requirements:**
- Single-line project description input
- AI-generated comprehensive checklist
- Includes: required permits, timeline, costs, considerations
- Downloadable as Markdown file
- Example projects for guidance
- Processing time: <10 seconds

**Acceptance Criteria:**
- [ ] User can describe project in one sentence
- [ ] Checklist includes all relevant permits
- [ ] Provides estimated timeline and costs
- [ ] Downloadable in Markdown format
- [ ] Includes next steps and considerations

---

#### 3.1.3 Council Meeting Summarizer
**Priority:** P1 (High)

**User Story:**
> As a community activist, I want to select my neighborhood and get relevant meeting summaries so that I can stay informed without reading entire transcripts.

**Requirements:**
- Dropdown with 61 San Diego neighborhoods
- Searchable neighborhood selection
- Text area for meeting transcript input
- AI-generated neighborhood-specific summary
- Downloadable summary as Markdown
- Filters irrelevant content automatically

**Acceptance Criteria:**
- [ ] Dropdown shows all 61 neighborhoods
- [ ] Search works within dropdown
- [ ] Summary extracts only relevant information
- [ ] Includes key decisions, projects, and action items
- [ ] Downloadable in Markdown format

---

### 3.2 Data Features (Must Have)

#### 3.2.1 Smart Data Loading
**Priority:** P0 (Critical)

**Requirements:**
- Automatic environment detection (local vs cloud)
- Local development uses downloaded CSV files
- Cloud deployment downloads from San Diego Open Data Portal
- Graceful fallback mechanisms
- Data validation and error handling
- Supports multiple file naming conventions

**Acceptance Criteria:**
- [ ] Works in local development environment
- [ ] Works on Streamlit Cloud without manual setup
- [ ] Falls back to URLs when local files unavailable
- [ ] Loads data within 30 seconds on first run
- [ ] Displays clear error messages on failure

---

#### 3.2.2 Real-Time Data Integration
**Priority:** P1 (High)

**Data Sources:**
- 257,692 active permits
- 132,550 closed permits
- 454,290 permit tags
- 61 community planning districts
- 9 council districts
- 124 police neighborhoods
- 3,677 zoning designations

**Requirements:**
- Data refreshed from source on deployment
- Displays data statistics in sidebar
- Data caching for performance
- Handles missing/malformed data

---

### 3.3 UI/UX Features (Must Have)

#### 3.3.1 Responsive Design
**Priority:** P0 (Critical)

**Requirements:**
- Works on desktop, tablet, mobile
- Dark mode support with proper contrast
- Chat input positioned at bottom
- Smooth animations and transitions
- Professional color scheme
- Accessible (WCAG 2.1 AA compliant)

**Acceptance Criteria:**
- [ ] Responsive on all screen sizes (320px - 2560px)
- [ ] Dark mode text is readable
- [ ] Chat input sticky at bottom
- [ ] No layout shifts on interaction
- [ ] Passes accessibility audit

---

#### 3.3.2 Example Questions & Templates
**Priority:** P1 (High)

**Requirements:**
- Pre-populated example questions
- Example project descriptions
- Quick-start buttons
- Helpful tooltips and hints
- Clear labels and placeholders

---

### 3.4 Nice-to-Have Features (Future)

#### 3.4.1 User Authentication
- Save conversation history
- Personalized recommendations
- Usage tracking per user

#### 3.4.2 Multi-language Support
- Spanish translation
- Other languages as needed

#### 3.4.3 Email/SMS Notifications
- Permit status updates
- Deadline reminders

#### 3.4.4 Advanced Search
- Filter permits by location
- Filter by date range
- Sort by various criteria

---

## 4. Technical Requirements

### 4.1 Performance
- Page load time: <3 seconds
- API response time: <5 seconds
- Data loading: <30 seconds on first run
- Support 100 concurrent users
- 99.5% uptime

### 4.2 Security
- API keys stored in environment variables
- No sensitive data in client-side code
- HTTPS only
- Rate limiting to prevent abuse
- Input sanitization

### 4.3 Scalability
- Handle 10,000+ users/month
- Automatic scaling on Streamlit Cloud
- Efficient data caching
- Optimized API calls

### 4.4 Browser Support
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### 4.5 Dependencies
- Python 3.8+
- Streamlit 1.30+
- Claude Sonnet 4.6 API
- Pandas 2.0+
- Internet connection for cloud deployment

---

## 5. Data Requirements

### 5.1 Data Sources
- San Diego Open Data Portal (primary)
- Local CSV files (development)
- Municipal code PDFs (supplementary)

### 5.2 Data Quality
- Data validated on load
- Missing values handled gracefully
- Regular updates from source
- Data accuracy monitoring

### 5.3 Data Privacy
- No personal user data collected
- No tracking without consent
- Compliant with data protection regulations

---

## 6. User Flows

### 6.1 New User - Ask Question Flow
1. User opens app
2. Sees welcome message and example questions
3. Types question or clicks example
4. Receives AI response within 5 seconds
5. Can ask follow-up questions
6. Session history maintained

### 6.2 Contractor - Generate Checklist Flow
1. User navigates to "Permit Checklist" tab
2. Reads example projects
3. Describes their project (one line)
4. Clicks "Generate Checklist"
5. Receives comprehensive checklist within 10 seconds
6. Reviews permits, timeline, costs
7. Downloads as Markdown file

### 6.3 Activist - Summarize Meeting Flow
1. User navigates to "Meeting Summary" tab
2. Selects neighborhood from dropdown (searchable)
3. Pastes meeting transcript
4. Clicks "Generate Summary"
5. Receives neighborhood-specific summary within 15 seconds
6. Reviews key decisions and action items
7. Downloads as Markdown file

---

## 7. Design Requirements

### 7.1 Visual Design
- Clean, modern interface
- Purple gradient header
- White/dark background (theme-aware)
- Professional typography
- Consistent spacing and alignment

### 7.2 Interaction Design
- Smooth transitions
- Loading indicators
- Clear error messages
- Helpful tooltips
- Intuitive navigation

### 7.3 Content Design
- Concise, clear copy
- Active voice
- Plain English (no jargon)
- Professional tone
- Helpful examples

---

## 8. Success Criteria

### 8.1 Launch Criteria
- [ ] All P0 features implemented and tested
- [ ] Data loading works in both environments
- [ ] 90%+ accuracy on test questions
- [ ] Performance meets requirements
- [ ] Security audit passed
- [ ] Documentation complete
- [ ] Deployed to Streamlit Cloud

### 8.2 Post-Launch Metrics (30 days)
- 500+ unique users
- 70%+ task completion rate
- 4.5+ average rating
- <$300 monthly API costs
- <1% error rate

---

## 9. Risks & Mitigations

### 9.1 Technical Risks

**Risk:** Claude API downtime
- **Impact:** High
- **Probability:** Low
- **Mitigation:** Display clear error message, retry logic, fallback responses

**Risk:** Data source unavailable
- **Impact:** Medium
- **Probability:** Low
- **Mitigation:** Local file fallback, cached data, graceful degradation

**Risk:** High API costs
- **Impact:** High
- **Probability:** Medium
- **Mitigation:** Caching, rate limiting, usage monitoring, prompt optimization

### 9.2 Product Risks

**Risk:** Low user adoption
- **Impact:** High
- **Probability:** Medium
- **Mitigation:** User testing, feedback loops, marketing, partnerships

**Risk:** Inaccurate responses
- **Impact:** High
- **Probability:** Medium
- **Mitigation:** Comprehensive testing, disclaimer, feedback mechanism, continuous improvement

---

## 10. Timeline & Milestones

### Phase 1: MVP (Complete)
- ✅ Basic Q&A functionality
- ✅ Permit checklist generator
- ✅ Meeting summarizer
- ✅ Local data loading

### Phase 2: Production (Complete)
- ✅ Cloud deployment
- ✅ URL-based data loading
- ✅ Dark mode support
- ✅ Improved UI/UX
- ✅ Comprehensive documentation

### Phase 3: Optimization (Current)
- [ ] Performance optimization
- [ ] Cost reduction strategies
- [ ] User feedback collection
- [ ] Analytics implementation

### Phase 4: Enhancement (Future)
- [ ] User authentication
- [ ] Advanced search
- [ ] Multi-language support
- [ ] Mobile app

---

## 11. Dependencies & Assumptions

### 11.1 Dependencies
- Anthropic Claude API availability
- San Diego Open Data Portal uptime
- Streamlit Cloud platform
- Internet connectivity (for cloud deployment)

### 11.2 Assumptions
- Users have internet access
- Users speak English
- San Diego Open Data Portal remains free
- Claude API pricing stays reasonable
- Streamlit Cloud remains free for public apps

---

## 12. Open Questions

1. Should we add user authentication for personalized features?
2. What is the acceptable response accuracy threshold?
3. How should we handle outdated permit information?
4. Should we add a feedback mechanism for incorrect responses?
5. What analytics should we track?

---

## 13. Approval & Sign-off

**Product Owner:** Kedar Kulkarni  
**Technical Lead:** Kedar Kulkarni  
**Status:** Approved  
**Date:** March 2026

---

## Appendix A: Glossary

- **Permit**: Official approval from San Diego Development Services for construction/renovation
- **Municipal Code**: Laws and regulations governing San Diego
- **RAG**: Retrieval-Augmented Generation - AI technique combining search with language generation
- **Community Planning District**: Geographic planning area in San Diego (61 total)
- **Council District**: Political representation area (9 total)

---

## Appendix B: References

- [San Diego Open Data Portal](https://data.sandiego.gov)
- [San Diego Development Services](https://www.sandiego.gov/development-services)
- [Anthropic Claude Documentation](https://docs.anthropic.com)
- [Streamlit Documentation](https://docs.streamlit.io)

---

**Document Control:**
- Version: 2.0.0
- Last Updated: March 2026
- Next Review: June 2026