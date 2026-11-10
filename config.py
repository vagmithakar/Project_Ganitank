## MODEL, LANGUAGES, AND LEVELS
## NOTES_SCHEMA
## NOTES_PROMPT
MODEL = "gemini-3.8-flash"
LANGUAGES = ["English", "Hindi", "Hinglish"]
LEVELS = ["Beginner", "Intermediate", "Advanced"]

NOTES_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "summary": {"type": "string"},
        "chapters": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "start": {
                        "type": "string",
                        "description": "Real start time as MM:SS or HH:MM:SS"
                    },
                    "heading": {"type": "string"},
                    "key_points": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["start", "heading", "key_points"]
            }
        },
        "key_terms": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "term": {"type": "string"},
                    "definition": {"type": "string"}
                },
                "required": ["term", "definition"]
            }
        }
    },
    "required": ["title", "summary", "chapters", "key_terms"]
}

NOTES_PROMPT = "Write short, concise point-wise notes for a {level} level and in {language} language"

FLASHCARD_SCHEMA = {
    "type": "object",
    "properties": {
        "cards": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "front": {
                        "type": "string",
                        "description": "A short question"
                    },
                    "back": {
                        "type": "string",
                        "description": "A 1-2 line answer"
                    }
                },
                "required": ["front", "back"]
            }
        }
    },
    "required": ["cards"]
}

FLASHCARD_PROMPT = "create {count} flashcards in {language}, made from {notes}. The front should be a short question, the back a 1-2 line answer. Use ONLY the notes."