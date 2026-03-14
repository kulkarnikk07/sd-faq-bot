# San Diego Permit FAQ Bot

An intelligent FAQ chatbot powered by Claude AI that helps users navigate San Diego's municipal permit system. This bot uses natural language processing and retrieval-augmented generation (RAG) to answer questions about permits, regulations, and procedures in San Diego.

## 🌟 Overview

The SD-FAQ-Bot is designed to simplify the process of obtaining information about San Diego municipal permits by providing instant, accurate responses to frequently asked questions. By leveraging Claude AI's advanced language understanding capabilities and a knowledge base derived from official San Diego municipal documents, the bot can assist residents, contractors, and businesses in understanding permit requirements and procedures.

## ✨ Features

- **Intelligent Q&A**: Uses Claude AI to understand and respond to natural language queries
- **Document-Based Knowledge**: Trained on official San Diego municipal permit documentation
- **Context-Aware Responses**: Provides relevant, accurate information based on the San Diego permit system
- **Easy to Use**: Simple chat interface for asking permit-related questions
- **Fast Response Time**: Quickly retrieves and processes information to answer queries

## 🏗️ Architecture

The bot is built with a modular architecture consisting of:

- **`app.py`**: Main application entry point and web interface
- **`bot.py`**: Core chatbot logic and Claude AI integration
- **`data_loader.py`**: Handles loading and processing of the San Diego municipal permit documentation
- **`sd_municipal.pdf`**: Source document containing official San Diego permit information

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Anthropic API key for Claude AI access
- pip package manager

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

3. **Set up environment variables**
   
   Create a `.env` file in the project root and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

## 📦 Dependencies

The project relies on the following key packages (see `requirements.txt` for complete list):

- **anthropic**: For Claude AI integration
- **PyPDF2** or **pdfplumber**: For parsing PDF documents
- **Flask** or **Streamlit**: For the web interface (depending on implementation)
- **python-dotenv**: For environment variable management

## 💡 Usage

Once the application is running, you can interact with the bot by:

1. Opening your web browser to the local server address (typically `http://localhost:5000` or similar)
2. Typing your question about San Diego permits in the chat interface
3. Receiving instant, AI-powered responses based on official documentation

### Example Questions

- "What permits do I need to build a fence in San Diego?"
- "How much does a building permit cost?"
- "What is the process for getting a mechanical permit?"
- "Do I need a permit for electrical work?"
- "How long does it take to get a permit approved?"

## 🔧 Configuration

The bot can be configured by modifying the following:

- **Document Source**: Update `sd_municipal.pdf` with the latest permit documentation
- **AI Model**: Adjust Claude model settings in `bot.py`
- **Response Parameters**: Fine-tune temperature, max tokens, and other AI parameters

## 📄 Data Source

The bot's knowledge is derived from the official San Diego municipal permit documentation (`sd_municipal.pdf`). This ensures that all responses are based on authoritative, up-to-date information about:

- Building permits
- Electrical permits
- Mechanical permits
- Plumbing permits
- Permit fees and costs
- Application procedures
- Timeline and processing information

## 🛠️ Development

### Project Structure

```
sd-faq-bot/
├── app.py              # Main application
├── bot.py              # Chatbot logic
├── data_loader.py      # Document processing
├── requirements.txt    # Python dependencies
├── sd_municipal.pdf    # Knowledge base document
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

### Adding New Features

To extend the bot's capabilities:

1. **Update the knowledge base**: Replace or add to `sd_municipal.pdf`
2. **Enhance bot logic**: Modify `bot.py` to add new response patterns
3. **Improve data processing**: Update `data_loader.py` for better document parsing

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available for use in accordance with applicable licensing terms.

## 🙏 Acknowledgments

- **Anthropic**: For providing Claude AI API
- **City of San Diego**: For permit documentation and information
- **Open Source Community**: For the tools and libraries that make this project possible

## 📧 Contact

For questions, suggestions, or issues, please open an issue on the GitHub repository.

## 🔗 Related Resources

- [City of San Diego Development Services](https://www.sandiego.gov/development-services)
- [San Diego Permit FAQs](https://www.sandiego.gov/development-services/permits/faqs)
- [Anthropic Claude AI Documentation](https://docs.anthropic.com/)

## ⚠️ Disclaimer

This bot provides information based on available documentation and should not be considered official legal or professional advice. Always verify important information with the City of San Diego Development Services Department or consult with appropriate professionals.

---

**Built with ❤️ using Claude AI**
