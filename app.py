import streamlit as st
import random

# ---- Echelon Framework Core (Simplified) ----

def check_laws(statement):
    laws_triggered = []
    s = statement.lower()

    if any(phrase in s for phrase in ["i think", "i believe", "in my opinion", "personally", "i feel"]):
        laws_triggered.append("LAW 1: Opinion Statement")
    if statement.strip().endswith("?"):
        laws_triggered.append("LAW 2: Question Asked")
    if "again and again" in s or "everyone says" in s:
        laws_triggered.append("LAW 3: Repetition Doesn't Increase Truth")
    return laws_triggered if laws_triggered else ["None"]

def classify_statement(statement):
    s = statement.lower()
    
    # General classification logic based on patterns
    if "obama is a muslim" in s:
        return {
            "echelon": "Misused Lie",
            "subtype": "Propaganda",
            "explanation": "This statement is a widely spread falsehood masquerading as fact, aiming to manipulate public opinion.",
            "laws": check_laws(statement)
        }
    
    elif "the earth is flat" in s:
        return {
            "echelon": "Misused Lie",
            "subtype": "Scientific Error",
            "explanation": "This statement is scientifically false. The Earth has been proven to be round.",
            "laws": check_laws(statement)
        }
    
    # Check if it's a fantastical statement
    elif "i am a dragon" in s or "i gave birth to the moon" in s:
        return {
            "echelon": "Absolute False",
            "subtype": "Fantasy Claim",
            "explanation": "This statement is detached from reality and is considered a fantasy claim.",
            "laws": check_laws(statement)
        }
    
    # Handle exaggerated metaphors like "capitalism is a weapon"
    elif "capitalism is a weapon" in s:
        return {
            "echelon": "Exaggerated Truth",
            "subtype": "Cultural Metaphor",
            "explanation": "This exaggerates the relationship between fatigue and capitalism as a metaphor, amplifying the critique.",
            "laws": check_laws(statement)
        }

    # Default if no specific classification matched
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

# Example statements with a rotation function
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

