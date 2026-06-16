# TechPickr - AI Smartphone Recommender

TechPickr is an intelligent AI-powered tech recommender that scrapes the latest live prices from the Indian market (Smartprix) and uses a powerful LLM to match the perfect device to your exact requirements. 

## Local Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your Groq API key:
   ```env
   GROQ_API_KEY=gsk_your_api_key_here
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
