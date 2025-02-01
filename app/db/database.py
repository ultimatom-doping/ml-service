import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "ml_database"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

student_collection = db.get_collection("students")
question_collection = db.get_collection("questions")
