
import streamlit as st
import random

# ---- Echelon Framework Core (Simplified) ----

def check_laws(statement):
    laws_triggered = []
    s = statement.lower()

    if any(phrase in s for phrase in ["i think", "i believe", "in my opinion", "personally", "i feel"]):
        laws_triggered.append("LAW 1")
        laws_triggered.append("LAW 3")
    if statement.strip().endswith("?"):
        laws_triggered.append("LAW 6")
    if "again and again" in s or "everyone says" in s:
        laws_triggered.append("LAW 7")
    return laws_triggered if laws_triggered else ["None"]

def classify_statement(statement):
    s = statement.lower()
    if "obama is a muslim" in s:
        return {
            "echelon": "Misused Lie",
            "subtype": "Propaganda",
            "explanation": "This statement disguises a disproven claim as opinion. It has been widely circulated in misinformation cycles.",
            "laws": check_laws(statement)
        }
    if "i am a dragon" in s or "i gave birth to the moon" in s:
        return {
            "echelon": "Absolute False",
            "subtype": "Fantasy Claim",
            "explanation": "This statement is detached from reality and contains fantastical or impossible elements.",
            "laws": check_laws(statement)
        }
    if "capitalism is a weapon" in s:
        return {
            "echelon": "Exaggerated Truth",
            "subtype": "Cultural Metaphor",
            "explanation": "This exaggerates a concept for rhetorical effect, tying fatigue to capitalism symbolically.",
            "laws": check_laws(statement)
        }
    return {
        "echelon": "Truth",
        "subtype": "Unspecified",
        "explanation": "No specific classification matched. Statement may need reevaluation.",
        "laws": check_laws(statement)
    }

# ---- UI ----

st.set_page_config(page_title="Truth Echelon Framework", page_icon="🧠")
st.title("🧠 Truth Echelon Framework")
st.markdown("Classify any public statement by **structure**, **function**, **distortion**, and **legal framing** using the **Truth Echelon Framework**.")

example_statements = [
    "The sky is purple because of vibes",
    "I’m a dragon IRL",
    "Stealing food is moral",
    "Barack Obama is a Muslim",
    "In my opinion, vaccines contain demons"
]

placeholder = random.choice(example_statements)
statement = st.text_area("🗣️ Enter a public statement", placeholder=placeholder)
submit = st.button("🧪 Classify Statement")

if submit and statement.strip():
    result = classify_statement(statement)
    st.success("✅ Classification Complete")
    st.header("🔍 Result")
    st.markdown(f"**Echelon:** {result['echelon']}")
    st.markdown(f"**Subtype:** {result['subtype']}")
    st.markdown(f"**Explanation:** {result['explanation']}")
    st.markdown(f"**Law Alert (if any):** {', '.join(result['laws'])}")
