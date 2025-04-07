
import streamlit as st
import openai
import os

# Set OpenAI API key securely
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Truth Echelon", layout="centered")

st.title("🧠 Truth Echelon Framework")
st.markdown("Classify any public statement by structure, function, and distortion using the **Truth Echelon Framework**.")

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


# Process input
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

        except Exception as e:
            st.error(f"Error: {e}")
