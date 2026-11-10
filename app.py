import streamlit as st
from gemini_client import get_client, extract_notes, make_flashcards
from config import LANGUAGES, LEVELS
from helpers import youtube_id

st.set_page_config(page_title="LectureLab", page_icon="🎓", layout="wide")

## dict {key : starting value}
DEFAULTS = {
    "link": None,
    "notes": None,
    "cards": None,
    "card_pos": 0,
    "flipped": False,
    "quiz": None,
    "quiz_problems": [],
    "quiz_submitted": False,
    "log": [],
}

def init_state():
    for key, value in DEFAULTS.items():
        if key not in st.session_state:   # sets ONLY The values not already present...
            st.session_state[key] = value.copy() if isinstance(value, list) else value

def reset_state():
    for key, value in DEFAULTS.items(): # sets ALL The values present IN THE LIST
        st.session_state[key] = value.copy() if isinstance(value, list) else value
    st.rerun()

def show_input_screen(client, level, language):
    link = st.text_input("Paste your youtube study material link here")
    
    if st.button("Build Study Kit"):
        if client is None:
            st.error("API Key missing. Add GEMINI_API_KEY to your .env file.")
            st.stop()
        else:
            if youtube_id(link) is None:
                st.warning("That doesn't look like a YouTube video link.")
                st.stop()
            else:
                video_id = youtube_id(link)
                st.session_state.link = "https://www.youtube.com/watch?v=" + video_id
                with st.spinner("Watching the lecture..."):
                    st.session_state.notes = extract_notes(client, st.session_state.link, level, language, st.session_state.log)
                st.rerun()

# PHASE 4- SHOW FLASHCARDS TAB:
def flip_card():
    st.session_state.flipped = not st.session_state.flipped

def next_card():
    st.session_state.card_pos += 1
    st.session_state.flipped = False

def show_flashcards_tab(client, count, language):
    if st.session_state.cards is None:
        if st.button("Generate Flashcards"):
            st.session_state.cards = make_flashcards(client, st.session_state.notes, count, language, st.session_state.log)
        st.rerun()
    cards = st.session_state.cards
    pos = st.session_state.card_pos % len(cards)
    card = cards[pos]

    # 3. Show the front or back
    if st.session_state.flipped:
        side, text = "ANSWER", card["back"]
    else:
        side, text = "QUESTION", card["front"]

    st.caption(f"Card {pos + 1} of {len(cards)} · {side}")
    with st.container(border=True):
        st.subheader(text)

    # 4. Two buttons in a row
    col1, col2 = st.columns(2)
    col1.button("Flip", on_click=flip_card)
    col2.button("Next", on_click=next_card)    
    
    
## ACTUALLY CALLING THE FUNCTION:
init_state()
client = get_client()


# Front-end logic

with st.sidebar:
    st.title("Settings")
    
    language = st.selectbox("Select preferred language: ", LANGUAGES)
    level = st.selectbox("Select level: ", LEVELS)
    flashcard_count = st.slider("Number of flashcards: ", 5, 20, 10)
    quiz_count = st.slider("Number of questions in a quiz: ", 3, 15, 5)
    
    # Adding a submit button
    if st.button("New video"):
        reset_state()

if st.session_state.notes is None:
    show_input_screen(client, level, language)
else:
    left_col, right_col = st.columns([2, 1])
    with left_col:
        st.subheader("Playing Video side-by-side...")
        st.video(st.session_state.link)
        
    with right_col:
        st.header(st.session_state.notes["title"])
        st.write(st.session_state.notes["summary"])

    # ADDING TABS FOR ALL COMPARTMENTS:        
    tab_cards, tab_quiz, tab_usage = st.tabs(["Flashcards", "Quiz", "Usage"])

    with tab_cards:
        show_flashcards_tab(client, flashcard_count, language)

    with tab_quiz:
        pass
        #show_quiz_tab(client, quiz_count, language)

    with tab_usage:
        pass
        #show_usage_tab()