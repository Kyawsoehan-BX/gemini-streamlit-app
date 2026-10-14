import os
import tempfile
from PIL import Image
import streamlit as st
from google import genai
from google.genai import types

# Page Setup
st.set_page_config(page_title="K AI Chat Studio", page_icon="⚡", layout="wide")

# API Key စစ်ဆေးခြင်း
api_key = os.environ.get("GEMINI_API_KEY")

with st.sidebar:
    st.title("⚙️ Settings")
    if not api_key:
        api_key = st.text_input("Enter Gemini API Key", type="password")
    
    lang = st.radio("🌐 Language / ဘာသာစကား", ["မြန်မာ", "English"])
    system_instruction = "You are a helpful and polite AI assistant. Always respond in Myanmar (Burmese) language." if lang == "မြန်မာ" else "You are a helpful and polite AI assistant."

if not api_key:
    st.info("👈 Please enter your Gemini API Key in the sidebar to get started.")
    st.stop()

# API Client ချိတ်ဆက်ခြင်း
client = genai.Client(api_key=api_key)

st.title("⚡ K AI Chat Studio")
st.caption("Multimodal Assistant powered by Google Gemini")

# Chat History သိမ်းဆည်းရန် setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# ရှိပြီးသား စကားပြောမှတ်တမ်းများ ပြသခြင်း
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input & File Upload
uploaded_file = st.file_uploader("Upload an Image or Video", type=["jpg", "jpeg", "png", "mp4"])
prompt = st.chat_input("Ask anything...")

if prompt:
    # User message ပြသခြင်း
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gemini သို့ ပေးပို့မည့် အချက်အလက်များ ပြင်ဆင်ခြင်း
    contents = [prompt]

    if uploaded_file is not None:
        if uploaded_file.type.startswith("image"):
            img = Image.open(uploaded_file)
            contents.append(img)
            st.image(img, caption="Uploaded Image", use_container_width=True)
        elif uploaded_file.type.startswith("video"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tfile:
                tfile.write(uploaded_file.read())
                temp_video_path = tfile.name
            video_file = client.files.upload(file=temp_video_path)
            contents.append(video_file)

    # Gemini ထံမှ အဖြေတောင်းယူခြင်း
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction
                    )
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")
