"""
Authors: Rohini
Date: 2024-06-01
"""
from ..utility import log_execution, logging
from ..storage_connection import MongodbOperations
from dwaraks.literatures.models import *
import os

mongodb_ops = MongodbOperations(db_name="ssb_library")
book_collection_name = "saisatcharitra"
sai_satcharitra_collection = mongodb_ops.get_collection(book_collection_name)
keys_to_remove = ["_id", "api_resource"] 

def ssc_about() -> str:
    try:
        sc_about = sai_satcharitra_collection.find({"api_resource": "about_ssb"})
        author_info = list(sc_about)[0].get('description', 'No author information available')
        return author_info
    except Exception as e:
        logging.error(f"Error retrieving about information for Srisai Satcharitra: {str(e)}")
        return "An error occurred while retrieving the about information."

def shirdi_sai_baba_about() -> dict:
    try:
        ssb_sc_about = sai_satcharitra_collection.find({"api_resource": "about_saibaba"})
        ssb_sc_about_info_dict = list(ssb_sc_about)[0]
        [ssb_sc_about_info_dict.pop(key, None) for key in keys_to_remove]  # Remove specified keys if they exist
        return ssb_sc_about_info_dict
    except Exception as e:
        logging.error(f"Error retrieving about information for Shirdi Sai Baba: {str(e)}")
        return "An error occurred while retrieving the about information."
    
def ssc_about_author() -> dict:
    try:
        sc_author = sai_satcharitra_collection.find({"api_resource": "about_ssb_author"})
        sc_author_info_dict = list(sc_author)[0]
        [sc_author_info_dict.pop(key, None) for key in keys_to_remove]  # Remove specified keys if they exist
        return sc_author_info_dict
    except Exception as e:
        logging.error(f"Error retrieving author information for Srisai Satcharitra: {str(e)}")
        return "An error occurred while retrieving the author information."
    
def insert_chapters(post_data : dict) -> str:
    try:
        print("Inserting chapter data into the database...")
        chapter_data = post_data.model_dump()  # Convert Pydantic model to dictionary
        chapter_number = chapter_data.get("chapter_number")
        if chapter_number is None:
            return "Chapter number is required."
        
        # Check if the chapter already exists
        existing_chapter = sai_satcharitra_collection.find_one({"chapter_number": chapter_number, 
                                                                "api_resource": "chapter"})
        if existing_chapter:
            return f"Chapter {chapter_number} already exists."
        
        try:
            # Insert the new chapter
            insert_message = mongodb_ops.insert_one(book_collection_name, chapter_data)
            return "success"
        except Exception as e:
            logging.error(f"Error inserting chapter to mongodb: {str(e)}")
            print(f"Error inserting chapter to mongodb: {str(e)}")
            return "error"
        
    except Exception as e:
        logging.error(f"Error inserting chapter: {str(e)}")
        print(f"Error inserting chapter: {str(e)}")
        return "error"


def update_chapter_details(chap_details: dict) -> str:
    try:
        chapter_number = chap_details.get("chapter_number")
        if chapter_number is None:
            return "Chapter number is required for update."
        
        # Check if the chapter exists
        existing_chapter = sai_satcharitra_collection.find_one({"chapter_number": chapter_number, 
                                                                "api_resource": "chapter"})
        if not existing_chapter:
            return f"Chapter {chapter_number} does not exist."
        
        try:
            # Update the chapter details
            update_result = mongodb_ops.update_one(
                {"chapter_number": chapter_number, "api_resource": "chapter"},
                {"$set": chap_details}
            )
            if update_result.modified_count > 0:
                return "success"
            else:
                return "No changes made to the chapter details."
        except Exception as e:
            logging.error(f"Error updating chapter in mongodb: {str(e)}")
            print(f"Error updating chapter in mongodb: {str(e)}")
            return "error"
        
    except Exception as e:
        logging.error(f"Error updating chapter details: {str(e)}")
        print(f"Error updating chapter details: {str(e)}")
        return "error"

def remove_chapter(chap_number: int) -> str:
    try:
        if chap_number is None:
            return "Chapter number is required for deletion."
        
        # Check if the chapter exists
        existing_chapter = sai_satcharitra_collection.find_one({"chapter_number": chap_number, 
                                                                "api_resource": "chapter"})
        if not existing_chapter:
            return f"Chapter {chap_number} does not exist."
        
        try:
            # Remove the chapter
            delete_result = mongodb_ops.delete_one(
                book_collection_name,
                {"chapter_number": chap_number, "api_resource": "chapter"}
            )
            if delete_result.deleted_count > 0:
                return "success"
            else:
                return "No chapter was deleted."
        except Exception as e:
            logging.error(f"Error deleting chapter from mongodb: {str(e)}")
            print(f"Error deleting chapter from mongodb: {str(e)}")
            return "error"
        
    except Exception as e:
        logging.error(f"Error removing chapter: {str(e)}")
        print(f"Error removing chapter: {str(e)}")
        return "error"