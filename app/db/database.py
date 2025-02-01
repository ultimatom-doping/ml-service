from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://dbUser:<1234>@cluster1-shard-00-00.jb8e9.mongodb.net:27017,cluster1-shard-00-01.jb8e9.mongodb.net:27017,cluster1-shard-00-02.jb8e9.mongodb.net:27017/?ssl=true&replicaSet=atlas-ki02iw-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster1")
DB_NAME = "ml_database"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

student_collection = db.get_collection("students")
question_collection = db.get_collection("questions")

