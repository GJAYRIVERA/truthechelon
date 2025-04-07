import streamlit as st
import random

# -----------------------------
# DAILY AND USER LIMIT SETTINGS
# -----------------------------
MAX_CALLS_PER_USER = 10

# -----------------------------
# LAW CHECKING SYSTEM
# -----------------------------
def check_laws(statement):
    laws = []
    s = statement.lower()
    if any(x in s for x in ["i feel", "i think", "in my opinion", "personally", "i believe"]):
        laws.append("LAW 1: The Claim Stands")
        laws.append("LAW 3: Emotional Framing Isn’t a Shield")
    if s.endswith("?"):
        laws.append("LAW 6: Function, Structure, Reach Define Tier")
    if any(x in s for x in ["everyone says", "they always", "all the time", "again and again"]):
        laws.append("LAW 7: Repetition Doesn’t Raise Tier")
    return laws if laws else ["None"]

# -----------------------------
# TRUTH ECHELON CLASSIFIER
# -----------------------------
def classify_statement(statement):
    s = statement.lower()

    # ABSOLUTE FALSE
    if any(x in s for x in ["i am a dragon", "i gave birth to the moon", "i am made of bees"]):
        return "Absolute False", "Fantasy Claim", "This statement is detached from reality or logic.", check_laws(statement)

    # MISUSED LIE
    if any(x in s for x in ["obama is a muslim", "earth is 6000 years old", "vaccines contain demons"]):
        return "Misused Lie", "Propaganda", "This is a widely debunked falsehood passed off as belief or fact.", check_laws(statement)

    # WHITE LIE
    if any(x in s for x in ["you look great", "i love your cooking", "i’m fine"]):
        return "White Lie", "Polite Praise", "A socially acceptable small falsehood to protect feelings.", check_laws(statement)

    # MORAL CONSTRUCT
    if any(x in s for x in ["killing is wrong", "respect your elders", "honesty is the best policy"]):
        return "Moral Construct", "Ethical Claim", "Unprovable but culturally or morally reinforced.", check_laws(statement)

    # EXAGGERATED TRUTH
    if any(x in s for x in ["i exploded", "everyone clapped", "worst day ever"]):
        return "Exaggerated Truth", "Hyperbole", "A real experience exaggerated for emotional impact.", check_laws(statement)

    # NEUTRAL
    if not s.strip() or len(s.split()) < 2 or s in ["hello", "yes", "no", "...", "okay"]:
        return "Neutral", "Filler", "Statement carries no truth value, judgment, or claim.", check_laws(statement)

    # BASIC TRUTH
    if any(x in s for x in ["i am", "this is my", "i went to", "i live in", "she’s my mom", "he is my friend"]):
        return "Basic Truth", "Personal Status", "A simple truth rooted in experience or lived identity.", check_laws(statement)

    # FIXED TRUTH
    if any(x in s for x in ["earth is round", "water boils", "humans need oxygen"]):
        return "Fixed Truth", "Scientific Fact", "A stable and accepted scientific or geographic truth.", check_laws(statement)

    # ABSOLUTE TRUTH
    if any(x in s for x in ["i exist", "1 equals 1", "energy cannot be destroyed"]):
        return "Absolute Truth", "Immutable Fact", "A universal, unchanging truth.", check_laws(statement)

    # CATCH: If nothing hit but it's still a sentence
    return "Neutral", "Unclassified", "No match found, but statement exists. Check logic or relevance.", check_laws(statement)

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="Truth Echelon Classifier", page_icon="🧠")
st.title("🧠 Truth Echelon Framework")
st.markdown("Classify any public statement using structural logic and social mapping.")

if "count" not in st.session_state:
    st.session_state.count = 0

if st.session_state.count >= MAX_CALLS_PER_USER:
    st.error("❌ Limit reached: You can only classify 10 statements per day.")
else:
    statement = st.text_area("💬 Enter a public statement")
    if st.button("🧠 Classify Statement") and statement.strip():
        echelon, subtype, explanation, laws = classify_statement(statement)
        st.session_state.count += 1

        st.success("✅ Classification Complete")
        st.markdown(f"**Echelon:** {echelon}")
        st.markdown(f"**Subtype:** {subtype}")
        st.markdown(f"**Explanation:** {explanation}")
        st.markdown(f"**Laws Triggered:** {', '.join(laws)}")

