import streamlit as st
import random

# -------------------------------
# Application Constants
# -------------------------------
LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Hindi": "hi",
    "Thai": "th"
}

EMOJIS = ["🎉", "🤩", "💡", "🏆", "😎", "🧠", "🎯"]

# -------------------------------
# Riddles Dataset
# -------------------------------
riddles = {
    "Easy": [
        {"question": "What has hands but can’t clap?", "answer": "a clock"},
        {"question": "What has to be broken before you can use it?", "answer": "an egg"},
        {"question": "What has a neck but no head?", "answer": "a shirt"},
        {"question": "What can run but never walks?", "answer": "water"}
    ],
    "Medium": [
        {"question": "What gets wetter the more it dries?", "answer": "a towel"},
        {"question": "What has one eye but can’t see?", "answer": "a needle"},
        {"question": "What has keys but can’t open locks?", "answer": "a piano"},
        {"question": "What can travel around the world while staying in a corner?", "answer": "a stamp"}
    ],
    "Hard": [
        {"question": "The more you take, the more you leave behind. What am I?", "answer": "footsteps"},
        {"question": "What comes once in a minute, twice in a moment, but never in a thousand years?", "answer": "the letter m"},
        {"question": "I speak without a mouth and hear without ears. What am I?", "answer": "an echo"},
        {"question": "What has a heart that doesn’t beat?", "answer": "an artichoke"}
    ]
}

# -------------------------------
# Game Logic Functions
# -------------------------------
def generate_riddle(level):
    return random.choice(riddles[level])

def evaluate_answer(user_input, correct_answer):
    return user_input.lower().strip() == correct_answer.lower().strip()

# -------------------------------
# Streamlit Config
# -------------------------------
st.set_page_config(page_title="Avery's Riddle Me This?", page_icon="🧠")

# -------------------------------
# Session State Initialization
# -------------------------------
for key, default in {
    'riddle': None,
    'score': 0,
    'attempts': 0,
    'language': "en",
    'hint_tokens': 3,
    'streak': 0,
    'user_riddle': None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:
    st.image("logo.jpg", width=150)
    st.title("📜 Game Info")

    st.subheader("🎯 Rules")
    st.markdown("""
    - Solve riddles and earn points  
    - Use hint tokens wisely  
    - Streaks = rewards!  
    - Stump your friends!
    """)

    st.subheader("📈 Progress")
    st.markdown(f"- **Score:** {st.session_state.score} / {st.session_state.attempts}")
    st.markdown(f"- **Streak:** {st.session_state.streak} 🔥")
    st.markdown(f"- **Hint Tokens:** {st.session_state.hint_tokens} 💡")

    if st.button("🔄 Reset Game"):
        st.session_state.score = 0
        st.session_state.attempts = 0
        st.session_state.streak = 0
        st.session_state.hint_tokens = 3
        st.session_state.riddle = None
        st.session_state.user_riddle = None
        st.success("Game reset! Try a new challenge!")

    st.subheader("🌐 Language")
    selected_lang = st.selectbox("Choose language:", list(LANGUAGES.keys()))
    st.session_state.language = LANGUAGES[selected_lang]

# -------------------------------
# Main App
# -------------------------------
st.title("🧠 Avery's Riddle Me This?")
st.image("logo.jpg", width=150)
st.markdown("Solve tricky riddles, earn trophies, and challenge your friends! 🎉")

mode = st.radio("Choose a mode:", ["🎲 Solve a Riddle", "🙃 Stump Your Friends"])

# -------------------------------
# Solve a Riddle Mode
# -------------------------------
if mode == "🎲 Solve a Riddle":
    level = st.selectbox("Choose your difficulty level:", ["Easy", "Medium", "Hard"])

    if st.button("🆕 New Riddle"):
        st.session_state.riddle = generate_riddle(level)

    if st.session_state.riddle:
        st.subheader("🧩 Riddle:")
        st.write(st.session_state.riddle["question"])

        user_input = st.text_input("Your answer:")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Submit Answer"):
                st.session_state.attempts += 1
                correct = evaluate_answer(user_input, st.session_state.riddle["answer"])
                if correct:
                    st.session_state.score += 1
                    st.session_state.streak += 1
                    emoji = random.choice(EMOJIS)
                    st.success(f"Correct! {emoji}")
                    st.balloons()
                    if st.session_state.streak % 3 == 0:
                        st.info("🏆 Streak reward! Bonus point!")
                        st.session_state.score += 1
                else:
                    st.session_state.streak = 0
                    st.error("Not quite! Try again or get a hint.")

        with col2:
            if st.button("💡 Use a Hint"):
                if st.session_state.hint_tokens > 0:
                    st.session_state.hint_tokens -= 1
                    answer = st.session_state.riddle["answer"]
                    hint = f"It starts with **'{answer[0]}'** and has {len(answer)} letters."
                    st.warning(hint)
                else:
                    st.warning("You’re out of hint tokens! Solve riddles to earn more.")

# -------------------------------
# Stump Your Friends Mode
# -------------------------------
elif mode == "🙃 Stump Your Friends":
    st.subheader("Challenge your friend to solve YOUR riddle!")

    custom_q = st.text_area("Enter your riddle (question):")
    custom_a = st.text_input("Enter the answer:")

    if st.button("🧠 Submit Custom Riddle"):
        if custom_q and custom_a:
            st.session_state.user_riddle = {"question": custom_q, "answer": custom_a}
            st.success("Riddle saved! Ask a friend to try solving it.")
        else:
            st.warning("Please provide both question and answer.")

    if st.session_state.user_riddle:
        st.markdown("---")
        st.subheader("Friend's Turn! 👯")
        st.write(st.session_state.user_riddle["question"])
        friend_input = st.text_input("What’s your guess?")
        if st.button("🎯 Submit Guess"):
            if evaluate_answer(friend_input, st.session_state.user_riddle["answer"]):
                st.success("You nailed it! 🎊")
            else:
                st.error("Nope, try again or ask for a hint!")

st.markdown("---")
st.markdown("**Built for Fun** | Created by ijones90002")
st.markdown("🎉 Keep playing to discover more riddles, win streak trophies, and become a riddle master!")
