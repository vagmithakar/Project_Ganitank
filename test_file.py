from gemini_client import get_client, extract_notes, make_flashcards
from helpers import youtube_id

client = get_client()
log = []   # a plain list here, since there is no st.session_state yet

link = "https://www.youtube.com/watch?v=yjtCQtADhDY"
video_id = youtube_id(link)
clean_link = "https://www.youtube.com/watch?v=" + video_id
notes = extract_notes(client, link, "Beginner", "English", log)

print(notes["title"])
for ch in notes["chapters"]:
    print(ch["start"], ch["heading"])

print(log)   # check that the call was recorded

cards = make_flashcards(client, notes, 5, "English", log)
print(len(cards))      # 5
print(cards[0])        # {'front': '...', 'back': '...'}
print(log)             # now 2 entries: notes and flashcards