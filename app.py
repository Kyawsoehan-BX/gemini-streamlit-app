import os
import tempfile
from PIL import Image
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="K AI Chat Studio", page_icon="⚡", layout="wide")

api_key = os.environ.get("GEMINI_API_KEY")

with st.sidebar:
    st.title("⚙️ Settings")
    if not api_key:
        api_key = st.text_input("Enter Gemini API Key", type="password")

if not api_key:
    st.warning("👈 Please enter your Gemini API Key in the sidebar to get started.")
    st.stop()

client = genai.Client(api_key=api_key)
