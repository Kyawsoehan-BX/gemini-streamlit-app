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

# Text Bar ပေါ်တွင် + (Attachment) icon တိုက်ရိုက်ပါရှိသော chat_input
chat_query = st.chat_input(
    placeholder=input_placeholder,
    accept_file=True,
    file_type=["jpg", "jpeg", "png", "webp", "mp4"]
)

if chat_query:
    user_text = chat_query.text if hasattr(chat_query, "text") and chat_query.text else ""
    user_files = chat_query.files if hasattr(chat_query, "files") and chat_query.files else []

    if user_text.strip() or len(user_files) > 0:
        file_preview = None
        file_type = None
        contents_payload = []

        # ဖိုင်ပါလာပါက ကိုင်တွယ်ခြင်း
        if len(user_files) > 0:
            uploaded_file = user_files[0]
            if "image" in uploaded_file.type:
                file_type = "image"
                img = Image.open(uploaded_file)
                file_preview = img
                contents_payload.append(img)
            elif "video" in uploaded_file.type:
                file_type = "video"
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name
                file_preview = tmp_path
                video_file_obj = client.files.upload(file=tmp_path)
                contents_payload.append(video_file_obj)

        if user_text.strip():
            contents_payload.append(user_text)
        else:
            fallback_prompt = "ဒီပုံ/ဗီဒီယိုထဲမှာ ဘာတွေပါလဲ၊ အသေးစိတ် သုံးသပ်ပြပါ။" if lang == "မြန်မာ" else "Analyze this image/video in detail."
            contents_payload.append(fallback_prompt)

        display_text = user_text if user_text.strip() else "(Attachment Sent)"
        
        # User မက်ဆေ့ခ်ျ မှတ်တမ်းတင်ခြင်း
        st.session_state.messages.append({
            "role": "user",
            "content": display_text,
            "file_preview": file_preview,
            "file_type": file_type
        })

        with st.chat_message("user", avatar=USER_AVATAR):
            if file_preview:
                if file_type == "image":
                    st.image(file_preview, width=300)
                elif file_type == "video":
                    st.video(file_preview)
            st.markdown(display_text)

        # AI ထံမှ အဖြေထုတ်ယူခြင်း
        with st.chat_message("assistant", avatar=BOT_AVATAR):
            with st.spinner(spinner_text):
                try:
                    response = client.models.generate_content(
                        model="%%writefile app.py
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import tempfile

# Page Setup
st.set_page_config(page_title="K AI Chat Studio", page_icon="⚡", layout="wide")

# API Client ချိတ်ဆက်ခြင်း
client = genai.Client(api_key="AQ.Ab8RN6I-H6OYQ9sVPcBrj-0FFNdpsUnAqU2JUe8CpyKlOM1FGg")

# Avatar Icons
USER_AVATAR = "https://cdn-icons-png.flaticon.com/512/3177/3177440.png"
BOT_AVATAR = "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"

# --- ဘေးဘက် Sidebar ---
with st.sidebar:
    st.image(BOT_AVATAR, width=70)
    st.title("Settings")

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

# --- ပင်မ Chat UI ---
st.title("⚡ AI Multimodal Studio")
st.caption(f"Role: **{bot_role}** | Language: **{lang}**")

if "messages" not in st.session_state:
    st.session_state.messages = []

# စကားပြောမှတ်တမ်း ပြန်လည်ပြသခြင်း
for msg in st.session_state.messages:
    avatar_icon = USER_AVATAR if msg["role"] == "user" else BOT_AVATAR
    with st.chat_message(msg["role"], avatar=avatar_icon):
        if "file_preview" in msg and msg["file_preview"]:
            if msg["file_type"] == "image":
                st.image(msg["file_preview"], width=300)
            elif msg["file_type"] == "video":
                st.video(msg["file_preview"])
        st.markdown(msg["content"])

# Text Bar ပေါ်တွင် 📎 Attachment icon ထည့်သွင်းထားသော chat_input
chat_query = st.chat_input(
    placeholder=input_placeholder,
    accept_file=True,
    file_type=["jpg", "jpeg", "png", "webp", "mp4", "mov"]
)

if chat_query:
    user_text = chat_query.text if chat_query.text else ""
    user_files = chat_query.files if chat_query.files else []

    # Text သို့မဟုတ် File တစ်ခုခုပါမှ စတင်အလုပ်လုပ်ခြင်း
    if user_text.strip() or len(user_files) > 0:
        file_preview = None
        file_type = None
        contents_payload = []

        # File ပါလာပါက ကိုင်တွယ်ခြင်း
        if len(user_files) > 0:
            uploaded_file = user_files[0]
            if "image" in uploaded_file.type:
                file_type = "image"
                img = Image.open(uploaded_file)
                file_preview = img
                contents_payload.append(img)
            elif "video" in uploaded_file.type:
                file_type = "video"
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name
                file_preview = tmp_path
                video_file_obj = client.files.upload(file=tmp_path)
                contents_payload.append(video_file_obj)

        if user_text.strip():
            contents_payload.append(user_text)
        else:
            # File တင်ပြီး စာမရိုက်ထားပါက default မေးခွန်း ပို့ပေးခြင်း
            fallback_prompt = "ဒီပုံ/ဗီဒီယိုထဲမှာ ဘာတွေပါလဲ၊ အသေးစိတ် သုံးသပ်ပြပါ။" if lang == "မြန်မာ" else "Analyze this image/video in detail."
            contents_payload.append(fallback_prompt)

        # ၁။ User မက်ဆေ့ခ်ျနှင့် ပုံ/ဗီဒီယိုကို ပြသခြင်း
        display_text = user_text if user_text.strip() else "(Attachment Sent)"
        st.session_state.messages.append({
            "role": "user",
            "content": display_text,
            "file_preview": file_preview,
            "file_type": file_type
        })

        with st.chat_message("user", avatar=USER_AVATAR):
            if file_preview:
                if file_type == "image":
                    st.image(file_preview, width=300)
                elif file_type == "video":
                    st.video(file_preview)
            st.markdown(display_text)

        # ၂။ AI ဆီမှ အဖြေထုတ်ယူခြင်း
        with st.chat_message("assistant", avatar=BOT_AVATAR):
            with st.spinner(spinner_text):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
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
        })",
                        contents=contents_payload,
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompts[bot_role]
                        )
                    )
                    ai_reply = response.text
                    st.markdown(ai_reply)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": ai_reply,
                        "file_preview": None,
                        "file_type": None
                    })
                except Exception as e:
                    st.error(f"Error: {e}")
