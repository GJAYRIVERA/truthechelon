import streamlit as st
import random

# ---- Echelon Framework Core (Simplified) ----

def check_laws(statement):
    laws_triggered = []
    s = statement.lower()

    # LAW 1: Opinion statement ("I think", "I believe", etc.)
    if any(phrase in s for phrase in ["i think", "i believe", "in my opinion", "personally", "i feel"]):
        laws_triggered.append("LAW 1: Opinion Statement")
    
    # LAW 2: Question is being asked
    if statement.strip().endswith("?"):
        laws_triggered.append("LAW 2: Question Asked")
    
    # LAW 3: Repetition doesn't increase truth
    if "again and again" in s or "everyone says" in s:
        laws_triggered.append("LAW 3: Repetition Doesn't Increase Truth")
    
    return laws_triggered if laws_triggered else []

def classify_statement(statement):
    s = statement.lower()
    
    # Misused Lie - Obama is Muslim
    if "obama is a muslim" in s:
        return {
            "echelon": "Misused Lie",
            "subtype": "Propaganda",
            "explanation": "This statement disguises a disproven claim as opinion. It has been widely circulated in misinformation cycles.",
            "laws": check_laws(statement)
        }
    
    # Misused Lie - Earth is flat
    elif "earth is flat" in s:
        return {
            "echelon": "Misused Lie",
            "subtype": "Scientific Error",
            "explanation": "This statement is scientifically false. The Earth has been proven to be round.",
            "laws": check_laws(statement)
        }
    
    # Absolute False - I am a dragon, or I gave birth to the moon
    elif "i am a dragon" in s or "i gave birth to the moon" in s:
        return {
            "echelon": "Absolute False",
            "subtype": "Fantasy Claim",
            "explanation": "This statement is detached from reality and is considered a fantasy claim.",
            "laws": check_laws(statement)
        }
    
    # Exaggerated Truth - Capitalism is a weapon
    elif "capitalism is a weapon" in s:
        return {
            "echelon": "Exaggerated Truth",
            "subtype": "Cultural Metaphor",
            "explanation": "This exaggerates the relationship between fatigue and capitalism as a metaphor, amplifying the critique.",
            "laws": check_laws(statement)
        }

    # Misused Lie - Vaccines contain demons (this should trigger as Misused Lie or Propaganda)
    elif "vaccines contain demons" in s:
        return {
            "echelon": "Misused Lie",
            "subtype": "Propaganda",
            "explanation": "This is a false and dangerous claim often used in misinformation cycles.",
            "laws": check_laws(statement)
        }

    # Basic Truth for statements about "my mom is my biological mom"
    elif "my mom is my biological mom" in s:
        return {
            "echelon": "Basic Truth",
            "subtype": "Factual Statement",
            "explanation": "This is a basic truth about one's biological mother. Can be verified through biological testing.",
            "laws": check_laws(statement)
        }

    # Absolute Truth - Statements that are universally verifiable, like "My mom gave birth to me."
    elif "my mom gave birth to me" in s:
        return {
            "echelon": "Absolute Truth",
            "subtype": "Historical Truth",
            "explanation": "This statement is verifiable through historical or personal accounts.",
            "laws": check_laws(statement)
        }
    
    # Default case: Always return the closest possible echelon
    return {
        "echelon": "Truth",
        "subtype": "Unspecified",  # Will refine this to a proper classification
        "explanation": "Statement does not match a predefined classification. Needs reevaluation.",
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

