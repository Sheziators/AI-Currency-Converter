# 💱 AI Currency Converter

An intelligent currency converter powered by Hugging Face LLM (Qwen 2.5) and real‑time exchange rates. Just ask naturally – *"Convert 100 USD to EUR"* – and get a beautifully formatted answer with live exchange rates.

![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-red?logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![LangChain](https://img.shields.io/badge/LangChain-0.4.0-green)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-LLM-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

- 🧠 **Natural Language Understanding** – Ask like you're talking to a friend
- 💱 **Real‑time Exchange Rates** – Powered by ExchangeRate‑API
- 🤖 **AI Tool Calling** – LLM intelligently fetches rates and calculates conversions
- 🎨 **Beautiful Chat Interface** – Currency symbols, formatted boxes, and persistent conversation history
- ⚡ **Instant Results** – No manual selection of currencies; just type your request
- 📜 **Conversation Persistence** – All your conversions stay visible even after new questions

## 🚀 Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

## 📋 Supported Currencies

The LLM can convert between **20+ major currencies** including:

| Code | Currency Name | Code | Currency Name |
|------|--------------|------|--------------|
| USD | US Dollar | EUR | Euro |
| GBP | British Pound | JPY | Japanese Yen |
| INR | Indian Rupee | CAD | Canadian Dollar |
| AUD | Australian Dollar | CHF | Swiss Franc |
| CNY | Chinese Yuan | SEK | Swedish Krona |
| NZD | New Zealand Dollar | MXN | Mexican Peso |
| SGD | Singapore Dollar | HKD | Hong Kong Dollar |
| NOK | Norwegian Krone | KRW | South Korean Won |
| TRY | Turkish Lira | RUB | Russian Ruble |
| BRL | Brazilian Real | ZAR | South African Rand |

## 🛠️ Technologies Used

- **Python 3.8+** – Core programming language
- **Streamlit** – Web application framework and chat UI
- **LangChain** – Tool binding and execution
- **Hugging Face** – Qwen 2.5‑7B‑Instruct LLM (free inference)
- **ExchangeRate-API** – Real‑time exchange rate data
- **Requests** – API communication

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- A [Hugging Face account](https://huggingface.co/) with an **access token** (free)

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/Sheziators/AI-Currency-Converter.git
cd AI-Currency-Converter
```

2. **Create virtual environment (recommended)**
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set your Hugging Face token as environment variable**
```bash
# Windows (PowerShell)
$env:HUGGINGFACEHUB_ACCESS_TOKEN="hf_your_token_here"

# Mac / Linux
export HUGGINGFACEHUB_ACCESS_TOKEN="hf_your_token_here"
```

5. **Run the application**
```bash
streamlit run app.py
```

6. **Open your browser** – Navigate to `http://localhost:8501`

## 🎯 Usage Guide

Simply **type your conversion request** in the chat, for example:

- `Convert 100 USD to EUR`
- `What is 50 GBP in INR?`
- `How much is 1000 Japanese Yen in US Dollars?`

The AI will automatically:
1. Detect the currencies and amount
2. Fetch the live exchange rate
3. Calculate the converted amount
4. Display a **beautiful formatted box** with:

✅ Conversion complete

| Amount | Exchange Rate | Converted |
|--------|--------------|-----------|
| $100.00 (USD) | 1 USD = 0.8589 EUR | €85.89 (EUR) |

📅 Last updated: real‑time

For **non‑conversion questions**, the AI answers in plain text like a normal chatbot.

## 📁 Project Structure

```
AI-Currency-Converter/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .gitignore            # Git ignore file
└── .streamlit/
    └── config.toml       # (Optional) Streamlit theme configuration
```

## 🔧 Configuration

### Hugging Face Token
The app requires a Hugging Face access token to use the free LLM inference API.

- **Locally**: Set environment variable `HUGGINGFACEHUB_ACCESS_TOKEN`
- **Streamlit Cloud**: Add it as a **secret** (Settings → Secrets)

### ExchangeRate-API Key
The app uses a **free tier** key already embedded (`754715f6d48aac37d37e5f25`). You can replace it with your own key in `app.py`:
```python
EXCHANGE_RATE_API_KEY = "your-api-key-here"
```

### Streamlit Configuration
Customize the app by editing `.streamlit/config.toml`:
- Theme colors
- Server settings
- Browser preferences

## 🚢 Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Select branch and main file (`app.py`)
5. In **Settings → Secrets**, add:
   ```
   HUGGINGFACEHUB_ACCESS_TOKEN = "hf_your_token_here"
   ```
6. Click **Deploy**

Your app will be live at `https://your-app-name.streamlit.app`.

### Deploy to Hugging Face Spaces

1. Create a new Space with **Streamlit SDK**
2. Upload `app.py` and `requirements.txt`
3. Add the token as a **secret** (Settings → Repository secrets)
4. Space will auto‑deploy

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add comments for complex logic (especially tool calling)
- Test locally with `streamlit run app.py`
- Update documentation as needed

## 🐛 Troubleshooting

### Common Issues

**Q: Hugging Face token not found?**
- Ensure you set the environment variable correctly or added the secret.
- The token must start with `hf_` and be valid.

**Q: LLM doesn't call tools correctly?**
- The model `Qwen/Qwen2.5-7B-Instruct` is finetuned for tool use.
- If it fails, try restarting the app.

**Q: Conversion rates not updating?**
- Check your internet connection.
- The free ExchangeRate-API has rate limits; wait a few seconds.

**Q: App not loading on Streamlit Cloud?**
- Verify `requirements.txt` includes all dependencies.
- Check that the Hugging Face secret is correctly named.

## 📝 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 AI Currency Converter

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co/) – for providing free LLM inference
- [ExchangeRate-API](https://www.exchangerate-api.com/) – for real‑time exchange rates
- [Streamlit](https://streamlit.io/) – for making UI development a joy
- [LangChain](https://www.langchain.com/) – for tool binding and orchestration

## 📧 Contact

Tathagat Shaw – tathagatshaw@gmail.com

Project Link: https://github.com/Sheziators/AI-Currency-Converter

## ⭐ Show Your Support

If you found this project helpful, please give it a ⭐ on GitHub!

---

Made with Intelligence for Businesses using Python, Streamlit, and Hugging Face LLMs
