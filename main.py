"""
@author: Rohini
created: 2024-04-27
@github: @arohini

"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from opentelemetry import trace
from opentelemetry import metrics
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from interceptor.metrics import *
from dwaraks.literatures.ssb_sc import chapters, get_chapter_title
from dwaraks.literatures.models import *
import logging, os
import uvicorn


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# 3. Instrument FastAPI
# This automatically tracks HTTP request counts, duration, and errors
FastAPIInstrumentor.instrument_app(app)


# Acquire a tracer
tracer = trace.get_tracer("spiritualdata.tracer")
# Acquire a meter.
meter = metrics.get_meter("spiritualdata.meter")

# Now create a counter instrument to make measurements with
hymn_counter = meter.create_counter(
    "spiritualdata.hymns",
    description="The number of spiritual hymns requested by users",
)

@app.get("/about/{author_name}")
def about_author(author_name: str) -> dict:
    """
    For the provided author_name , about information will be send as a response.

    Args:
        author_name (str): Provides info about the author

    Returns:
        dict: A dictionary containing the about information of the author
    """
    return {"message": f"About {author_name}"}


@app.get("/home")
def home():
    return {
        "message": "Welcome to the Scriptual Data Library. Explore and experience \
        the teachings, \
        stories, and experiences , Hymns related to Sadgurus and other spiritual \
            dieties."
    }


@app.get("/ssb-sc/index")
def get_ssb_index():
    return chapters


@app.get("/ssb-sc/chapter-name/{chapter_id}")
def get_chapter_name(chapter_id: int) -> dict:
    # Here you would typically fetch the chapter name for the given chapter_id
    # To do: from a database
    with tracer.start_as_current_span("ssb-sc-request") as hymn_span:
        logging.info(f"Received request for chapter ID: {chapter_id}")
        result = get_chapter_title(chapter_id)
        return result


@app.get("/data-list/{supreme-list}")
def get_divine_list(supreme_list: DivineList) -> dict:
    # Here you would typically fetch the divine list for the given supreme_list
    print(f"Received request for divine list: {supreme_list}")
    if supreme_list == DivineList.sai_baba:
        return {"divine_list": "ssb-sc refers to the Shirdi Sai Baba Satcharitra, \
            which is a sacred text that narrates the life, teachings, and miracles \
                of Shirdi Sai Baba. It is a revered scripture among devotees of Sai Baba \
                    and serves as a guide for spiritual growth and devotion."}
    elif supreme_list == DivineList.lord_ganesha:
        return {
            "divine_list": "API's provide a structured way to access and interact with \
            data, allowing developers to retrieve information about Lord Ganesha's stories,\
                teachings."
        }
    elif supreme_list == DivineList.lord_muruga:
        return {"divine_list": "API's blesses us with thirupugazh data, \
            which is a collection of Tamil devotional songs dedicated to Lord Muruga."}
    elif supreme_list == DivineList.lord_krishna:
        return {"divine_list": "This API guides us through the Bhagavad Gita, \
            a sacred Hindu scripture that is part of the Indian epic Mahabharata. \
            The Bhagavad Gita is a conversation between Prince Arjuna and Lord Krishna, \
                who serves"}
    else:
        raise HTTPException(status_code=404, detail="Divine list not found")


@app.get("/ssb-sc/chapter-content/{chapter_id:int}")
def get_chapter_content(chapter_id: int, content_limit: int = 500) -> dict:
    # Here you would typically fetch the chapter content for the given file path
    # To do: from a database or file system
    # data/ssb-sc/Sri-Sai-Satcharitra-English.pdf
    print(f"Received request for chapter ID: {chapter_id}")

@app.get("/lord-krishna/bhagavad-gita/download")
def download_bhagavad_gita():
    try:
        # Simulate a download request for the Bhagavad Gita
        logger.info("Received request to download the Bhagavad Gita")
        # Here you would typically fetch the file path from a database or file system
        file_path = "holywalls/lord-krishna/The_Bhagavad_Gita.pdf"
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise HTTPException(status_code=404, detail="File not found")
        
        logger.info(f"File found: {file_path}, preparing to send")
        file_path = "holywalls/lord-krishna/The_Bhagavad_Gita.pdf"
        return FileResponse(path=file_path, media_type="application/pdf", filename="The_Bhagavad_Gita.pdf")

    except Exception as e:      
        logger.error(f"Error occurred while processing the download request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    # Implementation for downloading the Bhagavad Gita

@app.get("/lord-krishna/vishnu-sahasranamam/download")
def download_vishnu_sahasranamam():
    try:
        # Simulate a download request for the Vishnu Sahasranamam
        logger.info("Received request to download the Vishnu Sahasranamam")
        # Here you would typically fetch the file path from a database or file system
        file_path = "holywalls/lord-krishna/Sri_Vishnu_Sahasranama_Stotram.pdf"
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise HTTPException(status_code=404, detail="File not found")
        
        logger.info(f"File found: {file_path}, preparing to send")
        return FileResponse(path=file_path, media_type="application/pdf", filename="Vishnu_Sahasranamam.pdf")

    except Exception as e:      
        logger.error(f"Error occurred while processing the download request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/lord_muruga/thirupugazh/download")
def download_thirupugazh():
    try:
        # Simulate a download request for the Thirupugazh
        logger.info("Received request to download the Thirupugazh")
        # Here you would typically fetch the file path from a database or file system
        file_path = "holywalls/lord-muruga/thiruppugazhmeipporulthelivuraipt-1.pdf"
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise HTTPException(status_code=404, detail="File not found")
        
        logger.info(f"File found: {file_path}, preparing to send")
        return FileResponse(path=file_path, media_type="application/pdf", filename="Thirupugazh.pdf")

    except Exception as e:      
        logger.error(f"Error occurred while processing the download request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/latitha-devi/lalitha-sahasranamam/download")
def download_lalitha_sahasranamam():
    try:
        # Simulate a download request for the Lalitha Sahasranamam
        logger.info("Received request to download the Lalitha Sahasranamam")
        # Here you would typically fetch the file path from a database or file system
        file_path = "holywalls/lalitha_devi/024_Shri_Lalita_Sahasra_Name_of_Shri_Ramamurti.pdf"
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise HTTPException(status_code=404, detail="File not found")
        
        logger.info(f"File found: {file_path}, preparing to send")
        return FileResponse(path=file_path, media_type="application/pdf", filename="Lalitha_Sahasranamam.pdf")

    except Exception as e:      
        logger.error(f"Error occurred while processing the download request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/lord_ganesha/ganesha_hymns/download")
def download_ganesha_stories():
    try:
        # Simulate a download request for the Ganesha Stories
        logger.info("Received request to download the Ganesha Stories")
        # Here you would typically fetch the file path from a database or file system
        file_path = "holywalls/lord-ganesha/Ganapati-Atharvashirsha-Upanishad.pdf"
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise HTTPException(status_code=404, detail="File not found")
        
        logger.info(f"File found: {file_path}, preparing to send")
        return FileResponse(path=file_path, media_type="application/pdf", filename="Ganesha_Stories.pdf")

    except Exception as e:      
        logger.error(f"Error occurred while processing the download request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/lord-shiva/thirumurai/download/{part_id}")
def download_thirumurai(part_id: str):
    try:
        # Simulate a download request for the Thirumurai
        logger.info("Received request to download the Thirumurai")
        # Here you would typically fetch the file path from a database or file system
        file_path = f"holywalls/lord-shiva/thiru0{part_id}_{part_id}.pdf"
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise HTTPException(status_code=404, detail="File not found")
        
        logger.info(f"File found: {file_path}, preparing to send")
        return FileResponse(path=file_path, media_type="application/pdf", filename="Thirumurai.pdf")

    except Exception as e:      
        logger.error(f"Error occurred while processing the download request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/lord-muruga/vel-maral/download")
def download_vel_maral():
    try:
        # Simulate a download request for the Vel Maral
        logger.info("Received request to download the Vel Maral")
        # Here you would typically fetch the file path from a database or file system
        file_path = "holywalls/lord-muruga/vel-maral.pdf"
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            raise HTTPException(status_code=404, detail="File not found")
        
        logger.info(f"File found: {file_path}, preparing to send")
        return FileResponse(path=file_path, media_type="application/pdf", filename="Vel_Maral.pdf")

    except Exception as e:      
        logger.error(f"Error occurred while processing the download request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    host = os.getenv("fastapi_host", "localhost")
    port = int(os.getenv("fastapi_port", 8000))
    uvicorn.run(app, host=host, port=port)
    
