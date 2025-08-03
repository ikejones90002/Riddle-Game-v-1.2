import streamlit as st
import requests
import random
from functools import lru_cache
import time

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
DEFAULT_LLM = "mistralai/Mixtral-8x7B-Instruct-v0.1"
FALLBACK_LLM = "facebook/bart-large"
SAFETY_LLM = "meta-llama/Llama-3.2-3B-Instruct" # Optional for additional features

# -------------------------------
# Riddles Dataset (Static)
# -------------------------------
riddles = {
    "Easy": [
        {"question": "What has hands but can’t clap?", "answer": "a clock"},
        {"question": "What has to be broken before you can use it?", "answer": "an egg"}
    ],
    "Medium": [
        {"question": "What gets wetter the more it dries?", "answer": "a towel"},
        {"question": "What has one eye but can’t see?", "answer": "a needle"}
    ],
    "Hard": [
        {"question": "The more you take, the more you leave behind. What am I?", "answer": "footsteps"},
        {"question": "What comes once in a minute, twice in a moment, but never in a thousand years?", "answer": "the letter m"}
    ]
}

# -------------------------------
# Safety Check
# -------------------------------
def check_safety(text, is_input=True):
    prompt = f"""
    Check if the following {'user input' if is_input else 'AI output'} is appropriate for a children's riddle game (fun, friendly, no inappropriate content). Return 'safe' if appropriate, or 'unsafe' with a brief reason.
    Text: {text}
    """
    result = ask_hugging_face(prompt, model=SAFETY_LLM)
    st.write(f"Debug: Safety check for '{text}' (is_input={is_input}): {result}")
    if result.startswith("⚠️"):
        st.warning(f"Debug: Safety check failed due to API error: {result}")
        return is_input  # Allow user input, block AI output if API fails
    return result.strip().lower().startswith("safe")

# -------------------------------
# Hugging Face API Function
# -------------------------------
@lru_cache(maxsize=100)
def ask_hugging_face(prompt, model=DEFAULT_LLM):
    if "huggingface" not in st.secrets or "api_key" not in st.secrets["huggingface"]:
        st.error("Hugging Face API key not found. Please add it under [huggingface] in Streamlit secrets.")
        return "⚠️ AI features are disabled. Please configure the API key."

    api_key = st.secrets["huggingface"]["api_key"]
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 30,  # Reduced to minimize rate limits
            "temperature": 0.7,
            "top_p": 0.9,
            "return_full_text": False
        }
    }
    
    models = [model, FALLBACK_LLM] if model == DEFAULT_LLM else [model]
    for current_model in models:
        try:
            response = requests.post(
                f"https://api-inference.huggingface.co/models/{current_model}",
                headers=headers,
                json=payload,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            if isinstance(result, list) and result and "generated_text" in result[0]:
                text = result[0]["generated_text"].strip()
                st.write(f"Debug: API response from {current_model}: {text}")
                return text
            elif isinstance(result, dict) and "generated_text" in result:
                text = result["generated_text"].strip()
                st.write(f"Debug: API response from {current_model}: {text}")
                return text
            elif isinstance(result, dict) and "text" in result:
                text = result["text"].strip()
                st.write(f"Debug: API response from {current_model}: {text}")
                return text
            elif isinstance(result, dict) and "error" in result:
                st.error(f"Debug: API Error for {current_model}: {result['error']}")
                if current_model == models[-1]:
                    return f"⚠️ API Error: {result['error']}"
                continue
            else:
                st.error(f"Debug: Unexpected API response format from {current_model}: {result}")
                if current_model == models[-1]:
                    return "⚠️ Unexpected response format from Hugging Face API."
                continue
        except requests.exceptions.RequestException as e:
            st.error(f"Debug: Failed to connect to Hugging Face API for {current_model}: {str(e)}")
            if current_model == models[-1]:
                return f"⚠️ Could not connect to Hugging Face AI: {str(e)}."
            time.sleep(2)
            continue
        except Exception as e:
            st.error(f"Debug: General error with Hugging Face API for {current_model}: {str(e)}")
            if current_model == models[-1]:
                return f"⚠️ An error occurred with the Hugging Face AI: {str(e)}."
            continue
    return "⚠️ All models failed."

# -------------------------------
# Conversational AI Function
# -------------------------------
def chat_with_ai(user_input, conversation_history):
    if not check_safety(user_input):
        return "⚠️ Sorry, that input isn't safe for this game! Try something else! 😊"
    
    personalities = [
        {"name": "Riddle Wizard", "tone": "magical and mysterious", "emoji": "🧙‍♂️"},
        {"name": "Puzzle Pal", "tone": "cheerful and encouraging", "emoji": "😄"},
        {"name": "Brainy Buddy", "tone": "smart and curious", "emoji": "🧠"}
    ]
    personality = random.choice(personalities)
    
    user_input_lower = user_input.lower().strip()
    response_type = "general"
    if any(word in user_input_lower for word in ["hint", "help", "clue"]):
        response_type = "hint"
    elif any(word in user_input_lower for word in ["why", "what", "how"]):
        response_type = "explanation"
    elif any(word in user_input_lower for word in ["good", "great", "awesome"]):
        response_type = "encouragement"
    
    riddle = st.session_state.riddle['question'] if st.session_state.riddle else "No riddle selected"
    prompt = f"""
    You are {personality['name']}, a friendly AI assistant for a kids' riddle game called 'Avery's Riddle Me This?'. 
    Respond in a {personality['tone']} tone, using emojis like {personality['emoji']} and keeping answers short (1-2 sentences). 
    The current riddle is: '{riddle}'.
    The conversation so far: {conversation_history}
    User: {user_input}
    
    Based on the user's input:
    - If they ask for a hint or help, give a short clue about the riddle.
    - If they ask a question (e.g., why, what, how), explain something fun related to the riddle or game.
    - If they say something positive (e.g., good, awesome), respond with encouragement.
    - Otherwise, reply with a fun, engaging comment related to the riddle or game.
    
    AI: """
    
    response = ask_hugging_face(prompt)
    if response.startswith("⚠️"):
        return f"Oops, my magic wand is stuck! Try again! {personality['emoji']}"
    return f"{response} {personality['emoji']}"

# -------------------------------
# Dynamic Riddle Generation
# -------------------------------
def generate_riddle(level):
    prompt = f"Generate a {level.lower()}-difficulty riddle for kids. Provide the riddle as a question and the answer separately, formatted as: Question: [riddle] Answer: [answer]. Keep it short and fun."
    response = ask_hugging_face(prompt)
    if response.startswith("⚠️") or not check_safety(response, is_input=False):
        return random.choice(riddles[level])
    try:
        question = response.split("Answer:")[0].replace("Question:", "").strip()
        answer = response.split("Answer:")[1].strip()
        return {"question": question, "answer": answer}
    except IndexError:
        return random.choice(riddles[level])

# -------------------------------
# Translate Riddle
# -------------------------------
def translate_riddle(riddle, language="es"):
    if language == "en":
        return riddle
    prompt = f"""
    Translate the following riddle question to {language}. Keep the tone fun and child-friendly. Only translate the question, not the answer.
    Riddle: {riddle['question']}
    """
    translated_question = ask_hugging_face(prompt)
    if translated_question.startswith("⚠️") or not check_safety(translated_question, is_input=False):
        return riddle
    return {"question": translated_question, "answer": riddle["answer"]}

# -------------------------------
# AI Answer Evaluator
# -------------------------------
def evaluate_answer(user_input, riddle_question, correct_answer):
    if not check_safety(user_input):
        return False
    prompt = f"""
    A child is solving a riddle.
    The riddle is: '{riddle_question}'
    The correct answer (in English) is: '{correct_answer}'.
    The child's answer is: '{user_input}'.
    Is the child's answer essentially correct, even if it's in a different language from the answer? Respond only with 'Yes' or 'No'.
    """
    reply = ask_hugging_face(prompt).strip().lower()
    return "yes" in reply

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

# Preload riddles
if not st.session_state.riddle_pool["Easy"]:
    for level in riddles:
        for _ in range(3):
            riddle = generate_riddle(level)
            if riddle:
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
        ask_hugging_face.cache_clear()
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
        if not st.session_state.riddle:
            st.session_state.riddle = random.choice(riddles[level])
        else:
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
                hint_level = "simple" if st.session_state.attempts < 3 else "detailed"
                prompt = f"Provide a {hint_level} hint for this riddle: {st.session_state.riddle['question']}. Keep it short and child-friendly."
                hint = ask_hugging_face(prompt)
                if hint.startswith("⚠️") or not check_safety(hint, is_input=False):
                    hint = "Think carefully about the words in the riddle! 😊"
                st.info(f"🧠 Hint: {hint}")

        with col3:
            if st.button("🤖 Ask the AI for help"):
                prompt = f"Help a child solve this riddle:\n\nRiddle: {st.session_state.riddle['question']}\n\nThey guessed: '{user_input}'. How should I help them?"
                ai_help = ask_hugging_face(prompt)
                if ai_help.startswith("⚠️") or not check_safety(ai_help, is_input=False):
                    ai_help = "Let's think about the riddle together! What's a key word in it? 😊"
                st.markdown(f"**AI says:** {ai_help}")

elif mode == "Stump the AI with your own riddle":
    st.subheader("🧙 Challenge the AI")
    custom_riddle = st.text_area("✍️ Type your own riddle for the AI:")
    if st.button("🤔 What’s your answer, AI?"):
        if custom_riddle.strip():
            if not check_safety(custom_riddle):
                st.warning("⚠️ That riddle isn't safe for this game! Try another one. 😊")
            else:
                prompt = f"A kid gave you this riddle. Try to solve it simply:\n\n{custom_riddle}"
                ai_answer = ask_hugging_face(prompt)
                if ai_answer.startswith("⚠️") or not check_safety(ai_answer, is_input=False):
                    ai_answer = "Hmm, that's a tricky one! Can you give me another riddle? 😊"
                st.markdown(f"**AI thinks:** {ai_answer}")
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
st.markdown("**Built with Hugging Face** | Created by ijones90002")