
from storage_connection import MongodbOperations
from bson.objectid import ObjectId
from fastapi import HTTPException, FastAPI
from datetime import datetime
from typing import Annotated
from dwaraks.literatures.models import JournalEntry

app = FastAPI()

mdo = MongodbOperations("ssb_library")



@app.get("/ssb-sc/experience-journal")
def get_experience_journal_entries():
    # Here you would typically fetch all experience journal entries from a database
    try:
        entries = mdo.get_collection("experience_journal").find().sort("date", -1) 
        # Sort by date in descending order
        # Convert MongoDB documents to Json-serializable format
        entries_list = []
        for entry in entries:
            entry["_id"] = str(entry["_id"])  # Convert ObjectId to string
            entries_list.append(entry)
        if entries_list:return entries_list[0]
        else: return {"message": "No experience journal entries found."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/ssb-sc/experience-journal")
def create_experience_journal(
    entry: Annotated[JournalEntry, "The content of the experience journal entry"]
):
    """
    Creates a new experience journal entry.
    Args:
        entry (JournalEntry): The content of the experience journal entry.
    Returns:
        dict: A message confirming the creation of the 
        experience journal entry and its reference ID.
    """
    author = entry.author
    econtent = entry.content
    chapter_number = entry.chapter_number
    date = entry.date
    entry_ref_id = f"{author}_{date.strftime('%Y%m%d%H%M%S')}"
    data = entry.model_dump()
    data["entry_ref_id"] = entry_ref_id
    print(f"Received experience journal entry: {data}")
    try:
        mdo.insert_one("experience_journal", data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # Here you would typically save the experience journal entry to a database
    return {"message": "Experience journal entry created successfully!", 
            "entry_ref_id": entry_ref_id}


@app.get("/ssb-sc/experience-journal/{entry_id}")
def get_experience_journal_entry(
    entry_id: Annotated[int, "The ID of the experience journal entry to retrieve"],
):
    """
    Retrieves a specific experience journal entry by its entry reference ID.
    Args:
    entry_id (str): The reference ID of the experience journal entry to retrieve.
    Returns:
    dict: The content of the experience journal entry.
    """
    # Here you would typically fetch the experience journal entry from a database
    return {
        "entry_id": entry_id,
        "content": "This is the content of the experience journal entry.",
    }


@app.put("/ssb-sc/experience-journal/{entry_id}")
def update_experience_journal_entry(
    entry_ref_id: Annotated[str, "The reference ID of the experience journal entry to update"],
    entry: Annotated[str, "The updated content of the experience journal entry"],
):
    """
    Updates the experience content from the journal entry for the given entry reference ID.
    Args:    
    entry_ref_id (str): The reference ID of the experience journal entry to update.
    entry (str): The updated content of the experience journal entry.
    Returns:    
    dict: A message confirming the update of the experience journal entry.
    """
    
    update_data = {
        "content": entry,
        "date": datetime.now()
    }
    try:        
        result = mdo.get_collection("experience_journal").update_one(
            {"entry_ref_id": entry_ref_id},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Experience journal entry not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # Here you would typically update the experience journal entry in a database
    return {
        "message": "Experience journal entry updated successfully!"
    }


@app.delete("/ssb-sc/experience-journal/{object_id}")
def delete_experience_journal_entry(
    object_id: Annotated[str, "The ID of the unique reference of the document"],
):
    """Deletes the experience journal entry with the given unique reference ID.
    Args:
        object_id (str): The unique reference ID of the experience journal entry to delete.
    Returns:
        dict: A message confirming the deletion of the experience journal entry."""
    try:
        ob_id = ObjectId(object_id)
        print(f"Received request to delete experience journal entry with ID: {ob_id}")
        result = mdo.get_collection("experience_journal").delete_one({"_id": ob_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Experience journal entry not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # Here you would typically delete the experience journal entry from a database
    return {
        "message": "Experience journal entry deleted successfully!",
        "object_id": object_id,
    }