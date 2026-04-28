"""
@author: Rohini
created: 2024-04-27
@github: @arohini

"""

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from config import uri

def atlas_health_check() -> None:
    """
    This function performs a health check on the MongoDB Atlas cluster by 
    attempting to connect and ping the server. It uses the connection URI 
    from the configuration file to establish a connection and sends a ping 
    command to confirm that the deployment is responsive. If the connection 
    is successful, it prints a success message; otherwise, it catches and 
    prints any exceptions that occur during the process.
    """
    
    try:
        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print("Error connecting to atlas MongoDB: " + str(e))
        
if __name__ == "__main__":
    atlas_health_check()