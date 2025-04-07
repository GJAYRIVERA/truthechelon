
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

# Load or reset usage
def load_usage():
    try:
        with open(USAGE_TRACK_FILE, "r") as f:
            data = json.load(f)
    except:
        data = {"date": str(datetime.today().date()), "global_count": 0}
    return data

def save_usage(data):
    with open(USAGE_TRACK_FILE, "w") as f:
        json.dump(data, f)

usage_data = load_usage()
if usage_data["date"] != str(datetime.today().date()):
    usage_data = {"date": str(datetime.today().date()), "global_count": 0}
    save_usage(usage_data)

# User session lock
if "user_count" not in st.session_state:
    st.session_state.user_count = 0
if "locked" not in st.session_state:
    st.session_state.locked = False

# UI setup
st.set_page_config(page_title="Truth Echelon", layout="centered")
st.title("🧠 Truth Echelon Framework")
st.markdown("Classify any public statement by **structure, function, distortion**, and **legal framing** using the Truth Echelon Framework.")

# Block if over user or global limit
if st.session_state.locked or st.session_state.user_count >= PER_USER_LIMIT:
    st.error("🚫 You’ve reached your 10-statement limit on this device. Thank you for testing!")
    st.stop()

if usage_data["global_count"] >= GLOBAL_DAILY_LIMIT:
    st.error("🚫 Daily usage limit for this app has been reached. Please come back tomorrow.")
    st.stop()

# Build classification prompt
def build_prompt(statement):
    return f"""You are the official classifier for the Truth Echelon Framework, a structural typology for public statements.

You must classify every input into:
- One of 12 official Echelons
- One matching Subtype (from the approved list)
- Provide an Explanation
- If applicable, state if a Truth Echelon Law is being invoked or violated (see below)
- Output must follow the exact structure below—do not alter it

Output Format:
Echelon: <Name>  
Subtype: <Subtype>  
Explanation: <1-2 sentence structured explanation>  
Law Alert (if any): <State which Truth Echelon Law applies or is being violated. If none, omit this line.>

Do NOT:
- Invent subtypes
- Merge labels or rename echelons
- Ramble or use run-on sentences

Truth Echelon Laws (summary):
LAW 1: The claim stands regardless of emotional tone.  
LAW 2: Intent doesn’t erase a statement’s structure.  
LAW 3: “In my opinion” or “I feel” does not shield a statement from classification.  
LAW 4: Context affects meaning.  
LAW 5: Both speaker and listener share the burden of clarity.  
LAW 6: Structure, function, and reach determine classification—not emotions.  
LAW 7: Repetition doesn’t make something truer.

Now classify the following public statement with precision and law awareness:

Statement: "{statement}"
"""


# Interface
statement = st.text_area("🗣️ Enter a public statement", placeholder="e.g., God said vaccines are poison", height=120)
submit = st.button("🧪 Classify Statement")

if submit and statement.strip() != "":
    with st.spinner("Analyzing truth structure..."):
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
