import streamlit as st
import random

# ---- Echelon Framework Core (Simplified) ----

def check_laws(statement):
    laws_triggered = []
    s = statement.lower()

    # Emotional framing
    if any(phrase in s for phrase in ["i think", "i believe", "in my opinion", "personally", "i feel"]):
        laws_triggered.append("LAW 1")
        laws_triggered.append("LAW 3")

    # If the statement ends with a question
    if statement.strip().endswith("?"):
        laws_triggered.append("LAW 6")

    # If statement repeats a claim (repetition)
    if "again and again" in s or "everyone says" in s:
        laws_triggered.append("LAW 7")

    # Return law alerts, or None if no laws are triggered
    return laws_triggered if laws_triggered else ["None"]

def classify_statement(statement):
    s = statement.lower()

    # Check specific statements and classify accordingly
    if "obama is a muslim" in s:
        return {
            "echelon": "Misused Lie",
            "subtype": "Propaganda",
            "explanation": "This statement disguises a disproven claim as opinion. It has been widely circulated in misinformation cycles.",
            "laws": check_laws(statement)
        }

    # Example of a fantasy claim
    if "i am a dragon" in s or "i gave birth to the moon" in s:
        return {
            "echelon": "Absolute False",
            "subtype": "Fantasy Claim",
            "explanation": "This statement is detached from reality and contains fantastical or impossible elements.",
            "laws": check_laws(statement)
        }

    # Exaggerated truths
    if "capitalism is a weapon" in s:
        return {
            "echelon": "Exaggerated Truth",
            "subtype": "Cultural Metaphor",
            "explanation": "This exaggerates a concept for rhetorical effect, tying fatigue to capitalism symbolically.",
            "laws": check_laws(statement)
        }

    # Default truth classification if no specific matches
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

# Pick a random statement to start with, if not previously entered
if "input_text" not in st.session_state:
    st.session_state.input_text = random.choice(example_statements)

# Allow user to input their statement and check if button is clicked
statement = st.text_area("🗣️ Enter a public statement", placeholder=st.session_state.input_text)

# Classify button
submit = st.button("🧪 Classify Statement")

# Process input if button is clicked
if submit and statement.strip():
    result = classify_statement(statement)
    
    st.success("✅ Classification Complete")
    st.header("🔍 Result")
    st.markdown(f"**Echelon:** {result['echelon']}")
    st.markdown(f"**Subtype:** {result['subtype']}")
    st.markdown(f"**Explanation:** {result['explanation']}")
    st.markdown(f"**Law Alert (if any):** {', '.join(result['laws'])}")
    
    # Save the statement in session state to persist
    st.session_state.input_text = statement

# Button to get a new random example statement
if st.button("Get New Example"):
    new_example = random.choice(example_statements)
    st.session_state.input_text = new_example  # Update session state with a new example
    st.text_area("🗣️ Enter a public statement", value=new_example, height=100)
