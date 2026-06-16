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

## Deploying to Streamlit Community Cloud (Free)

This application is perfectly optimized for **Streamlit Community Cloud**. To deploy it globally so anyone can use it:

1. **Upload to GitHub**:
   - Create a free account on [GitHub](https://github.com/) if you don't have one.
   - Create a new public repository.
   - Upload all the files in this folder to your new GitHub repository (make sure `.env` is NOT uploaded — the `.gitignore` file should prevent this automatically).

2. **Deploy the App**:
   - Go to [Streamlit Community Cloud](https://share.streamlit.io/).
   - Click **"New App"**.
   - Connect your GitHub account and select the repository you just created.
   - Set the Main file path to `app.py`.

3. **Add your API Keys (Crucial Step)**:
   - Before clicking deploy, click on **"Advanced Settings"**.
   - In the **Secrets** box, add your Groq API key exactly like this:
     ```toml
     GROQ_API_KEY = "gsk_your_api_key_here"
     ```
   - Click Save, then click **Deploy!**

Within 60 seconds, your AI app will be live on the internet with a public URL!
