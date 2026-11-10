import json
import os
import time
from google import genai
from dotenv import load_dotenv, GEMINI_API_KEY
from config import MODEL, NOTES_PROMPT, NOTES_SCHEMA, FLASHCARD_PROMPT, FLASHCARD_SCHEMA


load_dotenv()

def get_client():
    if(os.getenv("GEMINI_API_KEY")):
        return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
    else:
        return None
    
output = get_client()

if output is None:
    print("No API Key provided.") 
else:
    client = genai.Client() 
    interaction = client.interactions.create(    
            model="gemini-3.8-flash",    
            input=[        {"type": "text", "text": "Please summarize the video in 3 sentences."},
                           {"type": "video", "uri": "https://www.youtube.com/watch?v=yjtCQtADhDY"}    ] ) 
    
    #print(interaction.output_text)
     
    
#VIDEO PART:
def video_part(youtube_link):
    return {"type": "video", "uri": youtube_link}

#print(video_part("https://www.youtube.com/watch?v=dQw4w9WgXcQ"))


#Major functions like call_gemini & extract_notes
def call_gemini(client, contents, log, step, schema=None):
    start = round(time.time(), 2)
    
    if schema is None:
        interaction = client.interactions.create(model=MODEL, input=contents)

    else:
        interaction = client.interactions.create(model=MODEL, input=contents, response_format = {
                "type": "text",
                "mime_type": "application/json",
                "schema": schema,
            })

    seconds = round(time.time() - start, 2)
    log.append({"step": step, 
                "seconds": seconds, 
                "input_tokens": interaction.usage.total_input_tokens, 
                "output_tokens": interaction.usage.total_output_tokens})
    
    if schema is None:
        return interaction.output_text
    else:
        return json.loads(interaction.output_text)
    
    
#EXTRACT NOTES:
def extract_notes(client, youtube_link, level, language, log):
    prompt = NOTES_PROMPT.format(level = level, language = language)
    input_list = [video_part(youtube_link), {"type": "text", "text" : prompt}]
    return call_gemini(client, input_list, log, "notes", NOTES_SCHEMA)

def make_flashcards(client, notes, count, language, log):
    notes_text = json.dumps(notes)
    prompt = FLASHCARD_PROMPT.format(count=count, language=language, notes=notes_text)
    result = call_gemini(client, prompt, log, "flashcards", FLASHCARD_SCHEMA)
    return result["cards"]