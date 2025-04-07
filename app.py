
import streamlit as st
import openai
import os
import json
from datetime import datetime

# Set your OpenAI key from Streamlit Secrets
openai.api_key = os.getenv("OPENAI_API_KEY")

# Constants
PER_USER_LIMIT = 10
GLOBAL_DAILY_LIMIT = 2500
USAGE_TRACK_FILE = "usage_tracking.json"

# Load or initialize usage tracking
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

# Reset daily count if day has changed
usage_data = load_usage()
if usage_data["date"] != str(datetime.today().date()):
    usage_data = {"date": str(datetime.today().date()), "global_count": 0}
    save_usage(usage_data)

# Setup session state for per-user lock
if "user_count" not in st.session_state:
    st.session_state.user_count = 0
if "locked" not in st.session_state:
    st.session_state.locked = False

st.set_page_config(page_title="Truth Echelon", layout="centered")
st.title("🧠 Truth Echelon Framework")
st.markdown("Classify any public statement by structure, function, and distortion using the **Truth Echelon Framework**.")

# If user or global usage is maxed out
if st.session_state.locked or st.session_state.user_count >= PER_USER_LIMIT:
    st.error("🚫 You’ve reached your 10-statement limit on this device. Thank you for testing!")
    st.stop()

if usage_data["global_count"] >= GLOBAL_DAILY_LIMIT:
    st.error("🚫 Daily usage limit for this app has been reached. Please come back tomorrow.")
    st.stop()

# Input section
statement = st.text_area("📣 Enter a public statement", placeholder="Type something like 'All women lie' or 'The Earth is flat'...", height=100)
submit = st.button("🚀 Classify Statement")

# Prompt builder
def build_prompt(statement):
    return f"""You are a Truth Classification Engine operating under the Truth Echelon Framework, a structural system for classifying public statements by function, distortion, and context.

Instructions:
- Choose one of 12 Echelons.
- Choose one approved Subtype (do not invent).
- Give a short Explanation.
- Optionally include Function if applicable.
- Do not rename, modify, or invent echelon labels. Use only the official list.
- Do not assign "Developmental Error" unless the speaker is clearly a child or exhibits cognitive delay.
- Broad generalizations (e.g., “All women cheat”) = Misused Lie → Harmful Generalization.
- Absurd or surreal statements (e.g., “My face is my butt”) = Absolute False.
- Religious belief used in misinformation (e.g., “God said vaccines are evil”) = Misused Lie, not Moral Construct.

Echelons:
1. Absolute Truth
2. Fixed Truth
3. Basic Truth
4. Truth
5. Exaggerated Truth
6. Moral Construct
7. Neutral
8. False
9. White Lie
10. Lie
11. Misused Lie
12. Absolute False

Subtypes include:
Propaganda, Emotional Amplification, Harmful Generalization, Religious Literalism, Symbolic Metaphor, Scientific Fact, Developmental Error, Cultural Metaphor, Play Claim, Logical Collapse, etc.

Now classify this:

Statement: "{statement}"
"""


if submit and statement.strip() != "":
    with st.spinner("Classifying..."):
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": build_prompt(statement)}],
                temperature=0.4,
                max_tokens=500
            )
            result = response.choices[0].message.content.strip()
            st.success("✅ Classification Complete")
            st.markdown(f"""
### 🔍 Result  
{result}
""")
            # Update session and global usage counters
            st.session_state.user_count += 1
            usage_data["global_count"] += 1
            save_usage(usage_data)
            if st.session_state.user_count >= PER_USER_LIMIT:
                st.session_state.locked = True
        except Exception as e:
            st.error(f"Error: {e}")
