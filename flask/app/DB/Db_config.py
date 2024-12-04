import certifi
from pymongo import MongoClient
uri = "mongodb+srv://dlovej009:Dheeraj2006@cluster0.dnu8vna.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri,tlsCAFile=certifi.where())
db = client['PRINTER']
USER_collection = db['USERS']
PrintOwner_collection = db['PRINT_OWNER']
PrintRequest_collection = db['PRINT_REQUEST']