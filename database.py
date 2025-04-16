from mongoengine import connect
import os
from dotenv import load_dotenv



load_dotenv() 


MONGO_URI = os.getenv("MONGO_URI")
connect(db="support_db", host=MONGO_URI)

