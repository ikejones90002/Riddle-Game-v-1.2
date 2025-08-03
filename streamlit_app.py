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
# Static Functions
# -------------------------------
def generate_riddle(level):
    """Select a random riddle from the static dataset."""
    return random.choice(riddles[level])

def translate_riddle(riddle, language="es"):
    """Static version: Return the riddle as-is (no translation)."""
    return riddle

def evaluate_answer(user_input, riddle_question, correct_answer):
    """Check if the user's answer matches the correct answer (case-insensitive)."""
    return user_input.lower().strip() == correct_answer.lower().strip()

def chat_with_ai(user_input, conversation_history):
    """Generate static AI responses based on user input."""
    user_input_lower = user_input.lower().strip()
    riddle = st.session_state.riddle['question'] if st.session_state.riddle else "No riddle selected"
    personalities = [
        {"name": "Riddle Wizard", "emoji": "🧙‍♂️"},
        {"name": "Puzzle Pal", "emoji": "😄"},
        {"name": "Brainy Buddy", "emoji": "🧠"}
    ]
    personality = random.choice(personalities)

    # Predefined responses based on input type
    if any(word in user_input_lower for word in ["hint", "help", "clue"]):
        return f"Think about the key words in the riddle: {riddle}! {personality['emoji']}"
    elif any(word in user_input_lower for word in ["why", "what", "how"]):
        return f"That’s a great question! Focus on the clues in: {riddle}! {personality['emoji']}"
    elif any(word in user_input_lower for word in ["good", "great", "awesome"]):
        return f"You’re a riddle superstar! Keep it up! {personality['emoji']}"
    elif any(word in user_input_lower for word in ["riddle", "game", "fun"]):
        return f"This riddle game is a blast! Try guessing: {riddle}! {personality['emoji']}"
    else:
        return f"Let’s keep puzzling! What’s your next guess for: {riddle}? {personality['emoji']}"

# -------------------------------
# Streamlit App Config
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
    'conversation_history': [],
    'riddle_pool': {level: [] for level in riddles}
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Preload riddles into the pool
if not st.session_state.riddle_pool["Easy"]:
    for level in riddles:
        for _ in range(3):
            riddle = generate_riddle(level)
            st.session_state.riddle_pool[level].append(riddle)

# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:
    st.image("logo.jpg", width=150)
    st.title("📜 Game Info")
    st.subheader("🎯 Rules")
    st.markdown("""
    - Solve riddles or chat with the AI.
    - One answer per try.
    - Ask for hints or talk to the AI if stuck.
    """)
    st.subheader("🕹️ How to Play")
    st.markdown("""
    1. Choose a level  
    2. Select a language (optional)  
    3. Solve the riddle or chat with the AI  
    4. Submit answers or ask questions  
    5. Score points for correct answers!
    """)
    st.subheader("💡 Hints")
    st.markdown("""
    - Think about keywords.  
    - Break it down.  
    - Ask the AI for help! 😊
    """)
    st.subheader("📈 Progress")
    st.markdown(f"**Score:** {st.session_state.score} / {st.session_state.attempts}")
    if st.button("🔄 Reset Progress"):
        st.session_state.score = 0
        st.session_state.attempts = 0
        st.session_state.conversation_history = []
        st.success("Progress reset!")
    st.subheader("🌐 Language")
    lang_options = list(LANGUAGES.keys())
    lang_codes = list(LANGUAGES.values())
    selected_lang_name = st.selectbox(
        "Choose language:",
        options=lang_options,
        index=lang_codes.index(st.session_state.language)
    )
    st.session_state.language = LANGUAGES[selected_lang_name]

# -------------------------------
# Main App Content
# -------------------------------
st.title("🧠 Avery's Riddle Me This?")
st.image("logo.jpg", width=150)
st.markdown("Welcome to Avery's Riddle Me This? where you can solve riddles, chat with the AI, and have fun! 🎉")
level = st.selectbox("Choose your difficulty level:", ["Easy", "Medium", "Hard"])

if st.button("🎲 New Riddle"):
    if random.random() < 0.5 and st.session_state.riddle_pool[level]:
        st.session_state.riddle = random.choice(st.session_state.riddle_pool[level])
    else:
        st.session_state.riddle = generate_riddle(level)
        st.session_state.riddle_pool[level].append(st.session_state.riddle)
    if st.session_state.language != "en":
        st.session_state.riddle = translate_riddle(st.session_state.riddle, st.session_state.language)
    st.session_state.last_result = None
    st.session_state.conversation_history = []

mode = st.radio("Choose a mode:", ["Solve a riddle", "Stump the AI with your own riddle", "Chat with AI"])

if mode == "Solve a riddle":
    if st.session_state.riddle:
        st.subheader("🧩 Riddle:")
        st.write(st.session_state.riddle["question"])
        user_input = st.text_input("🔤 Type your answer:")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✅ Submit Answer"):
                st.session_state.attempts += 1
                is_correct = evaluate_answer(
                    user_input.strip(),
                    st.session_state.riddle["question"],
                    st.session_state.riddle["answer"]
                )
                if is_correct:
                    st.session_state.score += 1
                    st.success("🎉 That's correct! Great job!")
                    st.markdown(
                        f'<audio src="https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg" autoplay="true"></audio>',
                        unsafe_allow_html=True
                    )
                    st.balloons()
                else:
                    st.error("❌ Hmm... that's not quite right. Want a hint?")
                    st.markdown(
                        f'<audio src="https://actions.google.com/sounds/v1/cartoon/cartoon_boing.ogg" autoplay="true"></audio>',
                        unsafe_allow_html=True
                    )
        with col2:
            if st.button("💡 Hint"):
                hint = f"Think carefully about the words in the riddle: {st.session_state.riddle['question']}!"
                st.info(f"🧠 Hint: {hint}")
        with col3:
            if st.button("🤖 Ask the AI for help"):
                response = chat_with_ai(user_input, "\n".join(st.session_state.conversation_history))
                st.markdown(f"**AI says:** {response}")

elif mode == "Stump the AI with your own riddle":
    st.subheader("🧙 Challenge the AI")
    custom_riddle = st.text_area("✍️ Type your own riddle for the AI:")
    if st.button("🤔 What’s your answer, AI?"):
        if custom_riddle.strip():
            response = chat_with_ai(custom_riddle, "\n".join(st.session_state.conversation_history))
            st.markdown(f"**AI thinks:** {response}")
        else:
            st.warning("Please type a riddle first!")

elif mode == "Chat with AI":
    st.subheader("💬 Chat with the AI")
    st.markdown("Ask questions about the riddle, the game, or anything fun! 😄")
    user_chat = st.text_input("Type your message to the AI:")
    if st.button("📨 Send Message"):
        if user_chat.strip():
            st.session_state.conversation_history.append(f"User: {user_chat}")
            response = chat_with_ai(user_chat, "\n".join(st.session_state.conversation_history))
            st.session_state.conversation_history.append(f"AI: {response}")
            for message in st.session_state.conversation_history:
                st.markdown(message)
        else:
            st.warning("Please type a message first!")

st.markdown("---")
st.markdown("🗣️ Solve riddles, stump the AI, or chat for fun in the modes above!")
st.markdown("**Built for Fun** | Created by ijones90002")