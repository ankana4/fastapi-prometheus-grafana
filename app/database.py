from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.monitoring_db

users_collection = db.users
tasks_collection = db.tasks