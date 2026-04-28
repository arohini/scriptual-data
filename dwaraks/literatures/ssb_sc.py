"""
Authors: Rohini
Date: 2024-06-01
"""
from ..utility import log_execution, logging
import os

chapters = {
    1: "The Invocation",
    2: "The Purpose of the Narration and the Naming Ceremony",
    3: "The Consent Given to Write this Book",
    4: "The Appearance of Sai Samartha",
    5: "The Re-appearance of Sree Sai",
    6: "The Narration of the Story of Ram-janam Celebrations",
    7: "The Narration of Various Stories",
    8: "The Incarnation of Sai Samartha",
    9: "The Easiest Path (Untitled in original Marathi)",
    10: "The Greatness of Sree Sai Samartha",
    11: "The Description of Sree Sai's Greatness",
    12: "The Darshan of Ram – Sree Sant Gholap",
    13: "The Cure of Bhimaji's Tuberculosis",
    14: "Ruttonji's Meeting with Sai",
    15: "The Story of Cholkar's Sugar",
    16: "The Narration of the Knowledge of Brahman (Part 1)",
    17: "The Narration of the Knowledge of Brahman (Part 2)",
    18: "Favour that was Bestowed on Me (Part 1)",
    19: "Favour that was Bestowed on Me (Part 2)",
    20: "The Lesson of the Essence of the Ishavasya",
    21: "Bestowing Grace",
    22: "Warding Off of Untimely Death",
    23: "The Spectacle of the Leela of Guru and Disciple",
    24: "Splendid Humour",
    25: "Achieving the Devotee's Welfare by Granting Desires",
    26: "Prevention of Epilepsy and Suicide",
    27: "Bestowal of Initiation and Grace",
    28: "Narration of Visions",
    29: "Narration of Stories of Dreams",
    30: "Narration of Vows and Other Stories",
    31: "The Greatness of Darshan",
    32: "Narration of the Guru's Greatness",
    33: "The Power of the Udi",
    34: "The Greatness of Udi (Continued)",
    35: "The Erasure of Doubts and Misapprehensions",
    36: "The All-Pervasiveness of Sai and Fulfilment of Blessings",
    37: "Description of the Chavadi",
    38: "Description of the Cooking and the Vessel",
    39: "The Discourse on the Geeta and Creation of Samadhi Mandir",
    40: "The Narration of the Udyapan Story",
    41: "The Bestowal of Sai's Grace and Favour",
    42: "Leaving of the Body by Sainath (Part 1)",
    43: "Leaving of the Body by Sainath (Part 2)",
    44: "Leaving of the Body by Sainath (Part 3)",
    45: "The Greatness of the Feet of Sree Guru",
    46: "Trip to Kashi and Gaya",
    47: "Narration of Story Told by Sree Sai",
    48: "Granting of Favour to Doubting Devotee",
    49: "Testing the Saint and the Control of the Mind",
    50: "Removal of Ignorance",
    51: "A Triad of Stories of Three Devotees",
    52: "An Overall View / Summary",
    53: "Avataranika (Epitome)",
}

@log_execution
def get_chapter_title(chapter_id: int) -> dict:
    try:
        chapter_name = chapters.get(chapter_id, "Chapter not found")
        result = {"chapter_id": chapter_id, "chapter_name": chapter_name}
        return result
    except Exception as e:
        logging.error(f"Error retrieving chapter title for chapter ID: {chapter_id} - {str(e)}")
        return {"error": "An error occurred while retrieving the chapter title."}

def get_chapter_content(chapter_number: int) -> str:
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File not found")

    if not full_path.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Not a PDF file")

    try:
        reader = PdfReader(full_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return {
            "file": chapter_file,
            "content_preview": text[:content_limit],  # return only first 500 chars
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

