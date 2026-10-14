# User will input their own API Key or use secrets
import os
api_key = os.environ.get("GEMINI_API_KEY") or st.sidebar.text_input("Enter Gemini API Key", type="password")
client = genai.Client(api_key=api_key)
