
from functools import wraps
import uuid
from flask import session,redirect,url_for,request
from bson.objectid import ObjectId

# from app.DB.Db_config import collection

from app.DB.Db_config import USER_collection, PrintOwner_collection,PrintRequest_collection

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session :
            return func(*args, **kwargs)
        else:
            # Store the requested URL in the session before redirecting to login
            session['next_url'] = request.url
            return redirect(url_for('general_bp.login'))
    return wrapper
    


from azure.storage.blob import BlobServiceClient
import os

# Azure Blob Storage connection details
AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=tikuntectweb;AccountKey=hdRH71k9txeyWDLJNZiX/aE2UGGLvPjhDYaMzcDy5o48mdrUrDf1BTcNRbsqQyXPG8juWgTatZsl+AStK45Suw==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "printcu"

blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

def upload_document_to_blob(file):

        # Get a client for the container
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        # Generate a unique file name to avoid overwrites
        blob_client = container_client.get_blob_client(unique_filename)
        
        # Upload the file directly from the request
        blob_client.upload_blob(file.stream)
        
        # Return the URL of the uploaded blob
        return blob_client.url

from bson import ObjectId

def serialize(data):
    def convert_objectid(item):
        if isinstance(item, dict):
            return {k: convert_objectid(v) for k, v in item.items()}
        elif isinstance(item, list):
            return [convert_objectid(v) for v in item]
        elif isinstance(item, ObjectId):
            return str(item)
        else:
            return item

    # Check if data is a single object or a list
    if isinstance(data, list):
        return [convert_objectid(i) for i in data]
    elif isinstance(data, dict):
        return convert_objectid(data)
    else:
        return data
def current_user():
    # Check if the user is logged in
    if 'user_id' in session:
        user_id = session['user_id']

        # Retrieve user data from MongoDB using the user_id
        try:
            user_data = USER_collection.find_one({'_id':user_id}) or PrintOwner_collection.find_one({'_id':user_id})
            printer_requests = list(PrintRequest_collection.find({"_id": {"$in": user_data['print_requests']}}))
            pending_requests = [req for req in printer_requests if req['PrintsRequestStatus'] == False]
            user_data['status_pending']=pending_requests
            user_data['pending_requests_count'] = len(pending_requests)
            finished_requests = [req for req in printer_requests if req['PrintsRequestStatus'] == True]
            user_data['status_done']=finished_requests
            user_data['status_done_count'] = len(finished_requests)
        except:
            user_data['status_done_count']=0
            user_data['pending_requests_count']=0
            user_data['status_pending']=[]
            user_data['status_done']=[]

        return user_data
    
def user_by_id(id):
        user_data = USER_collection.find_one({'_id': id}) or PrintOwner_collection.find_one({'_id':id})
        if user_data:
            return user_data
        else:
            return None



