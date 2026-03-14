# 🏛️ San Diego Permit FAQ Bot

An intelligent AI-powered chatbot that helps users navigate San Diego's municipal permit system using real data from the City of San Diego Open Data Portal and Claude Sonnet 4.6.

---

## ✨ Features

### 💬 **Interactive Q&A Chat**
- Ask questions about San Diego permits in plain English
- Get instant, accurate responses powered by Claude Sonnet 4.6
- Context-aware answers based on real municipal code and permit data
- Conversation history with smooth chat interface

### ✅ **Permit Checklist Generator**
- Describe your project in one sentence
- Receive a customized permit checklist including:
  - Required permits
  - Estimated timelines
  - Approximate costs
  - Important considerations
  - Next steps
- Download checklist as Markdown file

### 📋 **Council Meeting Summarizer**
- Select from 61 San Diego neighborhoods
- Paste council meeting transcripts
- Extract neighborhood-specific information:
  - Key decisions affecting the community
  - Upcoming projects
  - Action items for residents
  - Important dates and deadlines
- Download summary as Markdown file

---

## 🚀 New Features (Latest Update)

### **Smart Data Loading**
- **Local Development**: Uses downloaded CSV files for fast loading
- **Cloud Deployment**: Automatically downloads data from San Diego Open Data Portal
- **Seamless Transition**: No configuration needed - works in both environments

### **Real San Diego Data**
- **390,000+ Permits**: Active and closed permit records
- **61 Neighborhoods**: Complete community planning districts
- **9 Council Districts**: City council representation data
- **124 Police Neighborhoods**: Detailed geographic coverage
- **3,600+ Zoning Designations**: Comprehensive zoning information

### **Enhanced UI/UX**
- ✅ Dark mode support with proper contrast
- ✅ Chat input at bottom (like modern messaging apps)
- ✅ Searchable neighborhood dropdown
- ✅ Responsive design for mobile and desktop
- ✅ Clean, professional interface with smooth animations

### **Developer Experience**
- Automatic fallback to remote data sources
- Flexible file structure support
- Comprehensive error handling
- Clear logging and status messages

---

## 🛠️ Tech Stack

- **AI Model**: Claude Sonnet 4.6 (Anthropic)
- **Web Framework**: Streamlit
- **Data Processing**: Pandas
- **Language**: Python 3.8+
- **Data Source**: San Diego Open Data Portal

---

## 📊 Data Sources

All data is sourced from official City of San Diego resources:

- [San Diego Open Data Portal](https://data.sandiego.gov)
- Development Services Department
- Community Planning Districts
- City Council Districts
- Municipal Code Documents

---

## 🏃 Quick Start

### Prerequisites

- Python 3.8 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/kulkarnikk07/sd-faq-bot.git
   cd sd-faq-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   
   Create a `.env` file in the project root:
   ```env
   ANTHROPIC_API_KEY=your_api_key_here
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   
   Navigate to `http://localhost:8501`

---

## 📁 Project Structure

```
sd-faq-bot/
├── app.py                      # Main Streamlit application
├── bot.py                      # Claude AI integration
├── data_loader.py              # Smart data loading (local/remote)
├── requirements.txt            # Python dependencies
├── .env                        # API key (create this)
├── .gitignore                  # Git ignore rules
├── data/                       # Local data files (optional)
│   ├── cmty_plan_datasd.csv
│   ├── council_districts_datasd.csv
│   ├── pd_neighborhoods_datasd.csv
│   ├── permits_set2_active_datasd.csv
│   ├── permits_set2_closed_datasd.csv
│   ├── permits_project_tags_datasd.csv
│   └── zoning_datasd.csv
└── README.md
```

---

## ☁️ Deployment to Streamlit Cloud

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Deploy to Streamlit Cloud"
git push origin main
```

### Step 2: Deploy on Streamlit
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repository: `kulkarnikk07/sd-faq-bot`
4. Main file: `app.py`
5. Click "Advanced settings" → "Secrets"
6. Add your API key:
   ```toml
   ANTHROPIC_API_KEY = "your-api-key-here"
   ```
7. Click "Deploy"

### Step 3: Automatic Data Loading
The app will automatically download data from San Diego Open Data Portal - no manual file uploads needed!

---

## 💡 Usage Examples

### **Ask a Question**
```
"What permits do I need to build a 200 square foot detached storage shed?"
```

### **Generate Checklist**
```
"I want to remodel my kitchen including new electrical outlets, 
relocating plumbing, and removing a non-load-bearing wall."
```

### **Summarize Meeting**
1. Select neighborhood: "Downtown"
2. Paste meeting transcript
3. Get neighborhood-specific summary

---

## 🎨 Features in Detail

### **Tab 1: Ask Questions**
- Natural language question input
- Real-time AI responses
- Conversation history
- Example questions for quick start
- Sources municipal code and permit data

### **Tab 2: Permit Checklist**
- One-line project description
- AI-generated comprehensive checklist
- Includes permits, timeline, costs
- Example projects provided
- Downloadable results

### **Tab 3: Meeting Summary**
- 61 San Diego neighborhoods in dropdown
- Searchable neighborhood selection
- Paste any council meeting content
- Extracts neighborhood-relevant info
- Download summary as file

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file:
```env
ANTHROPIC_API_KEY=your_api_key_here
```

### Streamlit Secrets (Cloud)

In Streamlit Cloud settings → Secrets:
```toml
ANTHROPIC_API_KEY = "your_api_key_here"
```

### Optional: Local Data Files

For faster local development, download CSV files from [data.sandiego.gov](https://data.sandiego.gov) and place in `data/` folder. The app will automatically use them instead of downloading.

---

## 🧪 Testing

### Test Data Loader
```bash
python data_loader.py
```

### Test Bot
```bash
python bot.py
```

### Test Full App
```bash
streamlit run app.py
```

---

## 📈 Data Statistics

Current dataset includes:
- **257,692** active permits
- **132,550** closed permits
- **454,290** permit tags
- **61** community planning districts
- **9** city council districts
- **124** police neighborhoods
- **3,677** zoning designations

*Data updated regularly from San Diego Open Data Portal*

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

---

## 🐛 Troubleshooting

### API Key Issues
- Verify key in `.env` file
- Check Streamlit Cloud secrets
- Ensure key is active at [console.anthropic.com](https://console.anthropic.com)

### Data Loading Issues
- Check internet connection (for cloud deployment)
- Verify CSV files in `data/` folder (for local)
- Check console logs for specific errors

### Neighborhood Dropdown Empty
- Ensure `data_loader.py` is updated
- Check that `cmty_plan_datasd.csv` loads correctly
- Run `python data_loader.py` to test

---

## 📝 License

This project is open source and available for educational purposes.

---

## ⚠️ Disclaimer

*This is a practice project created for educational purposes using publicly available data from the City of San Diego Open Data Portal. The information provided is for general guidance only and should not be considered official advice. Always verify permit requirements and regulations with the San Diego Development Services Department.*

---

## 👨‍💻 Developer

**Kedar Kulkarni**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/kedar-kulkarni/)

---

## 🙏 Acknowledgments

- **Anthropic** - For Claude AI API
- **City of San Diego** - For open data portal and resources
- **Streamlit** - For the amazing web framework
- **Open Source Community** - For tools and inspiration

---

## 📚 Resources

- [San Diego Open Data Portal](https://data.sandiego.gov)
- [San Diego Development Services](https://www.sandiego.gov/development-services)
- [Anthropic Claude Documentation](https://docs.anthropic.com)
- [Streamlit Documentation](https://docs.streamlit.io)

---

## 🔄 Changelog

### v2.0.0 (Latest)
- ✨ Added automatic data loading from URLs
- ✨ Fixed neighborhood dropdown (61 communities)
- ✨ Upgraded to Claude Sonnet 4.6
- ✨ Added dark mode support
- ✨ Improved chat interface (input at bottom)
- ✨ Added tech stack to About section
- 🐛 Fixed CSV loading for cloud deployment
- 🐛 Fixed data file path detection
- 📝 Updated documentation

### v1.0.0
- 🎉 Initial release
- 💬 Basic Q&A functionality
- ✅ Permit checklist generator
- 📋 Meeting summarizer

---

**Built with ❤️ for San Diego residents**

---

*For questions, issues, or suggestions, please [open an issue](https://github.com/kulkarnikk07/sd-faq-bot/issues) on GitHub.*
