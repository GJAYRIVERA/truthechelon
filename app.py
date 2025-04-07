import streamlit as st
import random

# -----------------------------
# DAILY AND USER LIMIT SETTINGS
# -----------------------------
MAX_CALLS_PER_USER = 10
TOTAL_COST_CAP = 2.00  # USD per day

# -----------------------------
# LAWS CHECKER
# -----------------------------
def check_laws(statement):
    laws = []
    s = statement.lower()
    if any(x in s for x in ["i feel", "i think", "in my opinion"]):
        laws.append("LAW 1: The Claim Stands")
        laws.append("LAW 3: Emotional Framing Isn’t a Shield")
    if s.endswith("?"):
        laws.append("LAW 6: Function, Structure, Reach Define Tier")
    if any(x in s for x in ["everyone says", "they always"]):
        laws.append("LAW 7: Repetition Doesn’t Raise Tier")
    return laws if laws else ["None"]

# -----------------------------
# STATEMENT CLASSIFIER
# -----------------------------
def classify_statement(statement):
    s = statement.lower()

    # ABSOLUTE FALSE
    if any(x in s for x in ["i am a dragon", "gave birth to the moon", "i am made of bees"]):
        return "Absolute False", "Fantasy Claim", "Detached from reality or logic.", check_laws(statement)

    # MISUSED LIE
    if any(x in s for x in ["obama is a muslim", "earth is 6000 years old"]):
        return "Misused Lie", "Propaganda", "Falsehood repeated without critical thinking.", check_laws(statement)

    # WHITE LIE
    if any(x in s for x in ["you look great", "i love your cooking"]):
        return "White Lie", "Polite Praise", "Social smoothing falsehood.", check_laws(statement)

    # MORAL CONSTRUCT
    if any(x in s for x in ["killing is wrong", "respect your elders"]):
        return "Moral Construct", "Ethical Claim", "Unprovable but value-based.", check_laws(statement)

    # EXAGGERATED TRUTH
    if any(x in s for x in ["i exploded", "everyone clapped"]):
        return "Exaggerated Truth", "Hyperbole", "Truth stretched for effect.", check_laws(statement)

    # NEUTRAL
    if not s.strip() or len(s.split()) < 2 or s in ["hello", "..."]:
        return "Neutral", "Filler", "No truth/false value.", check_laws(statement)

    # BASIC TRUTH
    if any(x in s for x in ["i am", "this is my", "i went to"]):
        return "Basic Truth", "Personal Status", "Lived and personal truth.", check_laws(statement)

    # FIXED TRUTH
    if any(x in s for x in ["earth is round", "water boils"]):
        return "Fixed Truth", "Scientific Fact", "Common knowledge that holds unless challenged deeply.", check_laws(statement)

    # ABSOLUTE TRUTH
    if any(x in s for x in ["i exist", "1 equals 1"]):
        return "Absolute Truth", "Existential", "Immutable across time.", check_laws(statement)

    # DEFAULT FALLBACK TO TRUTH IF NONE OF THE ABOVE BUT STILL VERIFIABLE
    return "Truth", "General", "Verifiable or reasoned truth.", check_laws(statement)

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="Truth Echelon Classifier", page_icon="🧠")
st.title("🧠 Truth Echelon Framework")
st.markdown("Classify any statement using structural truth mapping.")

# SESSION STATE SETUP
if "count" not in st.session_state:
    st.session_state.count = 0

if st.session_state.count >= MAX_CALLS_PER_USER:
    st.error("Daily limit reached. You may only classify 10 statements per day.")
else:
    statement = st.text_area("Enter a public statement:")
    if st.button("Classify") and statement.strip():
        echelon, subtype, explanation, laws = classify_statement(statement)
        st.session_state.count += 1

        st.success("Statement classified.")
        st.markdown(f"**Echelon:** {echelon}")
        st.markdown(f"**Subtype:** {subtype}")
        st.markdown(f"**Explanation:** {explanation}")
        st.markdown(f"**Laws Triggered:** {', '.join(laws)}")





