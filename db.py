from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')

cluster = MongoClient(MONGO_URI)

db = cluster['StudentDB']

student_collection = db['student']
major_collection = db['major']
