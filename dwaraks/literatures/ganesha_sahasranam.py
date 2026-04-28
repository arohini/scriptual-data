"""
@author: Rohini
created: 2024-04-27
@github: @arohini

"""

import re, os, datetime
from devatrans import DevaTrans
from deep_translator import GoogleTranslator
from sentence_transformers import SentenceTransformer
from huggingface_hub import login
from config import ganesha_sahasranamam_path, sankrit_embedding_model


#create DevaTrans object.
def sent_to_sanskrit(text: str) -> str:
    """
    This a function which converts the sentence provided in the paramater 
    to sanskrit text. If any error it will return sanskrit_version not found

    Args:
        text (str): The input text to be converted to Sanskrit

    Returns:
        str: The converted Sanskrit text or an error message
    """
    try:
        dt = DevaTrans()
        # Back-transliterate the input text to Devanagari script
        sanskrit_text = dt.back_transliterate(input_type="sen", from_convention="iast", sentence=text)
        return sanskrit_text
    except Exception as e:
        print(f"Error while back transliterating to sanksrit sentence: {e}")
        return "sanskrit_version not found"

def sanskrit_to_english_meaning(sans_text: str, source_lang: str = "sa", target_lang: str = "en") -> str:
    # TO DO: make source and target languages dynamic 
    # by passing as parameters to the function
    
    """
    This is a function which translates sanskrit input text provided to its 
    corresponding english meaning using google translator and returns translated text
    or an error message or no english meaning found

    Args:
        sans_text (str): The input Sanskrit text to be translated

    Returns:
        str: The translated English text or no english meaning found
    """
    try:
        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(sans_text)
        return translated
    except Exception as e:
        print(f"Error while translating Sanskrit to English: {e}")
        return "no english meaning found"

def clean_sanskrit(text: str) -> str:
    """This function takes a Sanskrit text as input and performs cleaning 
    operations on it. It removes double spaces, replaces vertical bars with 
    Purna Virama, and removes digits from the text. The cleaned text is then 
    returned. If any errors occur during the cleaning process, 
    they are printed to the console and the original text is returned.
    
    Args:
        text (str): "The input Sanskrit text to be cleaned"

    Returns:
        str: "The cleaned Sanskrit text"
    """
    corrections = {
        "  ": " ",     # Remove double spaces
        "|": "।",       # Fix vertical bars to Purna Virama
        "||": "॥"       # Fix double bars
    }
    for old, new in corrections.items():
        text = text.replace(old, new)
        text = re.sub(r'\d+', '', text)
    return text

# clean up the text by removing non-IAST characters and extra spaces
def clean_text(text: str) -> str:
    """This function takes a text input and performs cleaning operations on it. 
    It removes non-IAST characters, replaces multiple spaces with a single space,
    and applies additional Sanskrit-specific cleaning using the clean_sanskrit 
    function. If any errors occur during the cleaning process, 
    they are printed to the console and the original text is returned.

    Args:
        text (str): "The input text to be cleaned"

    Returns:
        str: "The cleaned text original text if an error occurs"
    """

    try:

        # Remove non-IAST characters (keep only letters, spaces, and common punctuation)
        cleaned_text = re.sub(r'[^a-zA-ZāīūṛḷṃḥñṭḍṇśṣĀĪŪṚḶṂḤÑṬḌṆŚṢ\s.,;॥!?-]', '', text)
        
        # Replace multiple spaces with a single space
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        
        cleaned_text = clean_sanskrit(cleaned_text)
        
        cleaned_text = cleaned_text.replace("॥ ॥", "॥")
        
        return cleaned_text
    except Exception as e:
        print(f"Error while cleaning text: {e}")
        return text

def stotram_from_text_file(file_path: str) -> list:
    """
    This function reads a text file containing stotram verses, 
    splits the content into individual verses based on the delimiter "॥", 
    and returns a list of cleaned verses. It also filters out any empty lines 
    or lines that do not contain valid IAST words. If any errors occur during the file reading process, they are printed to the console and an empty list is returned.

    Args:
        file_path (str): The path to the text file containing the stotram verses

    Returns:
        list: A list of cleaned stotram verses or an empty list if an error occurs
    """
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        
        # Split into lines and filter out empty lines
        lines = [clean_text(line.strip()) for line in text.split("॥") if line.strip()]
        
        # Assuming each line is a verse, we can return the list of verses
        return lines
    except Exception as e:
        print(f"Error while reading file: {e}")
        return []

    

def stotram_to_embeddings(verse: str) -> list:
    """
    For the embedding verse provided it will convert to numerical vestors based
    on the model selected and return the list of embeddings or empty list if any error 
    occurs.

    Args:
        verse (str): The input verse to be converted into embeddings

    Returns:
        list: A list of embeddings or an empty list if an error occurs
    """
    # This function would take the structured stotram and convert it to embeddings using a model like SentenceTransformer or similar.
    try:
        model = SentenceTransformer(sankrit_embedding_model)
        embeddings = model.encode(verse)
        return embeddings
    except Exception as e:
        print(f"Error while converting stotram to embeddings: {e}")
        return []

def structure_stotrams(verses: list) -> dict:
    """ This function takes a list of verses as input and processes each verse 
    to create a structured representation.
    
    For each verse, it performs the following steps:
    1. Converts the verse to Sanskrit using the sent_to_sanskrit function.
    2. Translates the Sanskrit version to English meaning using 
    the sanskrit_to_english_meaning function.
    3. Combines the Sanskrit version and English meaning into a single 
    text for embedding.
    4. Converts the combined text into embeddings using the 
    stotram_to_embeddings function.
    5. Appends a structured dictionary containing metadata, 
    verse number, Sanskrit text, 
    English meaning, and embeddings to the llm_structured_stotrams list.
    
    Finally, it returns the list of structured stotrams. 
    If any errors occur during the processing of the verses, they are printed 
    to the console and an empty list is returned.
    
    Args:
        verses (list): A list of verses to be structured
        Returns:
            dict: A dictionary containing the structured stotrams or an empty dictionary if an error occurs
    
    """
    start_time = datetime.datetime.now()
    try:
        llm_structured_stotrams = []
        for verse_no, verse in enumerate(verses):
            try:
                sanskrit_version = sent_to_sanskrit(verse)
            except Exception as e:
                print(f"Error while converting verse to Sanskrit: {e}")
                sanskrit_version = "sanskrit_version not found"
                
            try:
                english_meaning = sanskrit_to_english_meaning(sanskrit_version)
            except Exception as e:
                print(f"Error while translating Sanskrit to English: {e}")
                english_meaning = "english_meaning not found"
                
            # Combine names and meanings for a "Rich" embedding
            
            text_to_embed = f"{sanskrit_version} : {english_meaning}"
            try:
                embedding = stotram_to_embeddings(text_to_embed)
            except Exception as e:
                print(f"Error while converting stotram to embeddings: {e}")
                embedding = None
            
            llm_structured_stotrams.append({
                    "metadata": {
                    "deity": "Ganesha",
                    "source": "Ganesha Purana",
                    "stotram_name": "Ganesha Sahasranamam",
                    "author": "Bhāskara Rāya Mākhin",
                    "video_link": "https://youtu.be/AZeXlmORq48",
                    "timestamp": datetime.datetime.now().isoformat(),
                    "total_verses": len(verses),
                    },
                    "verse_no": verse_no + 1,
                    "sanskrit_text": sanskrit_version,
                    "english_meaning": english_meaning,
                    "embedding": embedding
                })
            
        end_time = datetime.datetime.now()
        print(f"Time taken to structure stotram: {end_time - start_time}")
        return llm_structured_stotrams
    except Exception as e:
        print(f"Error while structuring stotram: {e}")
        return []


if __name__ == "__main__":
    login(token=os.getenv("HF_TOKEN"))
    input_file_path = ganesha_sahasranamam_path
    verses = stotram_from_text_file(input_file_path)
    print(structure_stotrams(verses))