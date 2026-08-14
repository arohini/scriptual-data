"""
Authors: Rohini
Date: 2024-04-27
Description: This module defines the data models for the spiritual data application, 
including request and response schemas
"""

from pydantic import BaseModel, field_validator
from datetime import datetime
from enum import Enum

class ChapterRequest(BaseModel):
    id: int
    
class JournalEntry(BaseModel):
    content: str
    author: str
    chapter_number: int
    date: datetime | None = datetime.now()

class DivineList(str, Enum):
    sri_sai_baba = "sri-sai-baba"
    lord_ganesha = "lord-ganesha"
    lord_muruga = "lord-muruga"
    lord_krishna = "lord-krishna"
    lord_shiva = "lord-shiva"
    lord_hanuman = "lord-hanuman"
    goddess_lalitha = "goddess-lalitha"
    goddess_meenakshi = "goddess-meenakshi"
    goddess_durga = "goddess-durga"

class SubStory(BaseModel):
    sub_story_title: str
    sub_story_tag: str
    sub_story: str
class SaiSatcharitraChapter(BaseModel):
    chapter_number: int
    api_resource: str
    title: str
    tags : str
    stories: list[SubStory]
    
    @field_validator("chapter_number")
    def validate_chapter_number(cls, value):
        if value <= 0:
            raise ValueError("Chapter number must be a positive integer.")
        return value
    
    @field_validator("api_resource")
    def validate_api_resource(cls, value):
        if value != "chapter":
            raise ValueError("api_resource must be 'chapter'.")
        return value