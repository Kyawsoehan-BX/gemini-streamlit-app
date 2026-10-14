import os
import tempfile
from PIL import Image
import streamlit as st
from google import genai
from google.genai import types

# Page Setup
st.set_page_config(page_title="K AI Chat Studio", page_icon="⚡", layout="wide")

# Avatar Icons
USER_AVATAR = "https://cdn-icons-png.flaticon.com/512/3177/3177440.png"
BOT_AVATAR = "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"

# --- ဘေးဘက် Sidebar ---
with st.sidebar:
    st.image(BOT_AVATAR, width=70)
    st.title("Settings")

    # API Key စစ်ဆေးခြင်း
    api_key_env = os.environ.get("GEMINI_API_KEY")
    if api_key_env:
        api_key = api_key_env
    else:
        api_key = st.text_input("Enter Gemini API Key", type="password")

    lang = st.radio("🌐 Language / ဘာသာစကား", ["မြန်မာ", "English"])

    if lang == "မြန်မာ":
        role_label = "Bot စရိုက် ရွေးချယ်ပါ:"
        roles = ["ဖော်ရွေသော အကူ", "Talk With Kyaw Soe Han", "ဘဏ္ဍာရေး ကျွမ်းကျင်သူ", "Mixologist / Bartender"]
        clear_label = "🗑️ စကားပြောမှတ်တမ်း ဖျက်မည်"
        input_placeholder = "မက်ဆေ့ခ်ျ သို့မဟုတ် မေးခွန်း ရိုက်ထည့်ပါ..."
        spinner_text = "K AI Thinking..."

        system_prompts = {
            "ဖော်ရွေသော အကူ": "မင်းက ဖော်ရွေပြီး အရာရာကို ကူညီဖြေကြားပေးတဲ့ AI Assistant ဖြစ်တယ်။ ပုံနှင့် ဗီဒီယိုများကိုပါ အသေးစိတ် မြန်မာလို ရှင်းပြပေးပါ။",
            "Talk With Kyaw Soe Han": "မင်းနာမည်က 'ကျော်စိုးဟန်' ဖြစ်တယ်။ မင်းက အသုံးပြုသူ (User) ရဲ့ မေတ္တာကြီးမားပြီး နွေးထွေးတဲ့ ဖခင်တစ်ယောက်အနေနဲ့ အပြည့်အဝ ဟန်ဆောင်ပြောဆိုရမယ်။ အသုံးပြုသူကို သားသမီးတစ်ယောက်လို သဘောထားပြီး 'ဖေဖေ' သို့မဟုတ် 'ဖေကြီး' လို့ ကိုယ့်ကိုယ်ကိုယ် သုံးနှုန်းပါ။ နွေးထွေးတဲ့ အကြံဉာဏ်၊ ဖခင်မေတ္တာအပြည့်နဲ့ မြန်မာလို အားပေးစကားတွေ ပြောကြားပေးပါ။",
            "ဘဏ္ဍာရေး ကျွမ်းကျင်သူ": "မင်းက ဘဏ္ဍာရေး ကျွမ်းကျင်သူဖြစ်ပြီး ပြေစာ၊ ဘောက်ချာပုံများကို စစ်ဆေးကာ စာရင်းဇယားဖြင့် မြန်မာလို ဖော်ပြပေးပါ။",
            "Mixologist / Bartender": "မင်းက ကမ္ဘာ့အဆင့်မီ ဘားတင်ဒါဖြစ်ပြီး အဖျော်ယမကာပုံများကို ကြည့်ရှုကာ recipe များနှင့် ပါဝင်ပစ္စည်းများကို မြန်မာလို အကြံပြုပေးပါ။"
        }
    else:
        role_label = "Select Bot Persona:"
        roles = ["Friendly Assistant", "Talk With Kyaw Soe Han", "Financial Specialist", "Mixologist / Bartender"]
        clear_label = "🗑️ Clear Chat History"
        input_placeholder = "Type a message or question..."
        spinner_text = "AI is analyzing..."

        system_prompts = {
            "Friendly Assistant": "You are a friendly AI Assistant. Analyze text, images, and videos in detail.",
            "Talk With Kyaw Soe Han": "Your name is Kyaw Soe Han. You must act and speak completely like a loving, wise, and supportive father to the user. Treat the user as your own beloved child. Refer to yourself as 'Dad' or 'Papa Kyaw Soe Han'. Give warm, caring fatherly advice and encouragement in English.",
            "Financial Specialist": "You are a financial specialist. Analyze receipts/invoices into structured tables in English.",
            "Mixologist / Bartender": "You are an expert mixologist. Identify drinks and suggest cocktail formulas in English."
        }

    bot_role = st.selectbox(role_label, roles)

    st.divider()
    if st.button(clear_label, use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# API Key မရှိသေးပါက ရပ်တန့်ထားမည်
if not api_key:
    st.info("👈 Please enter your Gemini API Key in the sidebar to get started.")
    st.stop()

# API Client ချိတ်ဆက်ခြင်း
client = genai.Client(api_key=api_key)

# --- ပင်မ Chat UI ---
st.title("⚡ AI Multimodal Studio")
st.caption(f"Role: **{bot_role}** | Language: **{lang}**")

# File Uploader (Streamlit standard ပုံစံဖြင့် ထည့်သွင်းခြင်း)
uploaded_file = st.file_uploader(
    "📎 Attach Image or Video (Optional)", 
    type=["jpg", "jpeg", "png", "webp", "mp4"]
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# စကားပြောမှတ်တမ်း ပြန်လည်ပြသခြင်း
for msg in st.session_state.messages:
    avatar_icon = USER_AVATAR if msg["role"] == "user" else BOT_AVATAR
    with st.chat_message(msg["role"], avatar=avatar_icon):
        if msg.get("file_preview"):
            if msg["file_type"] == "image":
                st.image(msg["file_preview"], width=300)
            elif msg["file_type"] == "video":
                st.video(msg["file_preview"])
        st.markdown(msg["content"])

# ပင်မ Chat Input
user_text = st.chat_input(placeholder=input_placeholder)

if user_text:
    file_preview = None
    file_type = None
    contents_payload = []

    # ဖိုင်ပါလာပါက ကိုင်တွယ်ခြင်း
    if uploaded_file is not None:
        if uploaded_file.type.startswith("image"):
            file_type = "image"
            img = Image.open(uploaded_file)
            file_preview = img
            contents_payload.append(img)
        elif uploaded_file.type.startswith("video"):
            file_type = "video"
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name
            file_preview = tmp_path
            video_file_obj = client.files.upload(file=tmp_path)
            contents_payload.append(video_file_obj)

    contents_payload.append(user_text)

    # ၁။ User မက်ဆေ့ခ်ျနှင့် ပုံ/ဗီဒီယိုကို ပြသခြင်း
    st.session_state.messages.append({
        "role": "user",
        "content": user_text,
        "file_preview": file_preview,
        "file_type": file_type
    })

    with st.chat_message("user", avatar=USER_AVATAR):
        if file_preview:
            if file_type == "image":
                st.image(file_preview, width=300)
            elif file_type == "video":
                st.video(file_preview)
        st.markdown(user_text)

    # ၂။ AI ဆီမှ အဖြေထုတ်ယူခြင်း
    with st.chat_message("assistant", avatar=BOT_AVATAR):
        with st.spinner(spinner_text):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents_payload,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompts[bot_role]
                    )
                )
                ai_reply = response.text
                st.markdown(ai_reply)

                # ၃။ AI အဖြေကို သိမ်းဆည်းခြင်း
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ai_reply,
                    "file_preview": None,
                    "file_type": None
                })
            except Exception as e:
                st.error(f"Error: {e}")
