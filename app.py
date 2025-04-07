import streamlit as st
import random

# ---- Echelon Framework Core (Simplified) ----

def check_laws(statement):
    laws_triggered = []
    s = statement.lower()

    # LAW 1 and LAW 3 for Opinion Statement
    if any(phrase in s for phrase in ["i think", "i believe", "in my opinion", "personally", "i feel"]):
        laws_triggered.append("LAW 1")  # Opinion statement
        laws_triggered.append("LAW 3")  # Emotional framing law
    
    # LAW 6 for questions
    if statement.strip().endswith("?"):
        laws_triggered.append("LAW 6")
    
    # LAW 7 for repetitive statements or generalizations
    if "again and again" in s or "everyone says" in s:
        laws_triggered.append("LAW 7")
    
    return laws_triggered if laws_triggered else ["None"]


def classify_statement(statement):
    s = statement.lower()

    # Check for known problematic or special cases
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
    if "vaccines contain demons" in s:
        return {
            "echelon": "Misused Lie",
            "subtype": "Conspiracy Theory",
            "explanation": "This statement spreads a widely debunked conspiracy theory, lacking evidence and rational basis.",
            "laws": check_laws(statement)
        }
    if "capitalism is a weapon" in s:
        return {
            "echelon": "Exaggerated Truth",
            "subtype": "Cultural Metaphor",
            "explanation": "This exaggerates a concept for rhetorical effect, tying fatigue to capitalism symbolically.",
            "laws": check_laws(statement)
        }

    # Handle Neutral statements (meaningless input)
    if not s.strip() or len(s.split()) < 2:
        return {
            "echelon": "Neutral",
            "subtype": "Nonsense",
            "explanation": "This statement is meaningless or too vague to classify into a truth or falsehood category.",
            "laws": check_laws(statement)
        }

    


# ---- UI ----

st.set_page_config(page_title="Truth Echelon Framework", page_icon="🧠")
st.title("🧠 Truth Echelon Framework")
st.markdown("Classify any public statement by **structure**, **function**, **distortion**, and **legal framing** using the **Truth Echelon Framework**.")

# Example statements with a rotation function
example_statements = [
    "The sky is purple because of vibes",
    "I’m a dragon IRL",
    "Stealing food is moral",
    "Barack Obama is a Muslim",
    "In my opinion, vaccines contain demons",
    "Earth is flat",
    "Capitalism is a weapon"
]

# Ensure session state stores the user's input and provide a default statement
if "input_text" not in st.session_state:
    st.session_state.input_text = random.choice(example_statements)

# Allow user to input their statement and check if button is clicked
statement = st.text_area("🗣️ Enter a public statement", value=st.session_state.input_text)

# Classify button
submit = st.button("🧪 Classify Statement")

# Process input if button is clicked
# Properly handle the result output after classification
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

