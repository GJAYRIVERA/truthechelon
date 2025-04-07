
import streamlit as st
import openai
import os
import json
from datetime import datetime

# Set OpenAI key securely
openai.api_key = os.getenv("OPENAI_API_KEY")

# Constants
PER_USER_LIMIT = 10
GLOBAL_DAILY_LIMIT = 2500
USAGE_TRACK_FILE = "usage_tracking.json"

def load_usage():
    try:
        with open(USAGE_TRACK_FILE, "r") as f:
            return json.load(f)
    except:
        return {"date": str(datetime.today().date()), "global_count": 0}

def save_usage(data):
    with open(USAGE_TRACK_FILE, "w") as f:
        json.dump(data, f)

usage_data = load_usage()
if usage_data["date"] != str(datetime.today().date()):
    usage_data = {"date": str(datetime.today().date()), "global_count": 0}
    save_usage(usage_data)

if "user_count" not in st.session_state:
    st.session_state.user_count = 0
if "locked" not in st.session_state:
    st.session_state.locked = False

st.set_page_config(page_title="Truth Echelon", layout="centered")
st.title("🧠 Truth Echelon Framework")
st.markdown("Classify any public statement by **structure**, **function**, **distortion**, and **legal framing** using the **Truth Echelon Framework**.")

if st.session_state.locked or st.session_state.user_count >= PER_USER_LIMIT:
    st.error("🔒 You've reached your 10-statement limit on this device.")
    st.stop()

if usage_data["global_count"] >= GLOBAL_DAILY_LIMIT:
    st.error("📉 Daily usage limit reached. Try again tomorrow.")
    st.stop()

# New improved prompt
def build_prompt(statement):
    return f"""You are the classifier for the Truth Echelon Framework.

Classify each input using:
- One of these EXACT echelons (do NOT invent): Absolute Truth, Fixed Truth, Basic Truth, Truth, Exaggerated Truth, Moral Construct, Neutral, False, White Lie, Lie, Misused Lie, Absolute False.
- One of the 5 official subtypes tied to that echelon (do NOT make new ones).
- Follow this strict format with clear structure and legal alerts.

Strictly enforce:
- "Opinion", "Belief", "Perspective", "Feeling" do NOT override classification.
- Never rename echelons. Do not use "Opinion" or "Personal Belief" as echelons.
- If the user tries to bypass truth by saying "I feel..." or "my opinion", raise LAW 1 and LAW 3.

Format:
Echelon: <One of the 12 official categories>  
Subtype: <One of the official subtypes>  
Explanation: <Why it lands here>  
Law Alert (if any): <Cite LAW 1, 2, 3, etc. or leave blank>

Statement: "{statement}"
"""


statement = st.text_area("🗣️ Enter a public statement", placeholder="e.g., Obama is a Muslim", height=120)
submit = st.button("🧪 Classify Statement")

if submit and statement.strip():
    with st.spinner("Processing..."):
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": build_prompt(statement)}],
                temperature=0.3,
                max_tokens=500
            )
            result = response.choices[0].message.content.strip()
            st.success("✅ Classification Complete")
            st.markdown(f"### 🔍 Result\n{result}")
            st.session_state.user_count += 1
            usage_data["global_count"] += 1
            save_usage(usage_data)
            if st.session_state.user_count >= PER_USER_LIMIT:
                st.session_state.locked = True
        except Exception as e:
            st.error(f"⚠️ API error: {e}")
