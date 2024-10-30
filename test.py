from flask import Flask, json, request, jsonify, render_template
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

# Azure Blob Storage connection details
AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=printxd;AccountKey=Pz1cNIgzVh25s5Ipcicxj/VBIeFaVgv8WVB0OqRz29kqUHU44Ymrr0Rkg4GF/ejQcikRa7SYrhqH+AStppjSHA==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "printcu"

# Initialize the BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

def upload_document_to_blob(file):
    try:
        # Get a client for the container
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        
        # Use the file's original name (or you can generate a unique name)
        blob_client = container_client.get_blob_client(file.filename)
        
        # Upload the file stream directly to Azure Blob
        blob_client.upload_blob(file.stream)
        
        # Return the URL of the uploaded blob
        return blob_client.url

    except Exception as e:
        print(f"Error uploading document: {e}")
        return None

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Upload the PDF file to Azure Blob Storage
    uploaded_url = upload_document_to_blob(file)
    
    if uploaded_url:
        return jsonify({"message": "File uploaded successfully", "url": uploaded_url}), 200
    else:
        return jsonify({"error": "Upload failed"}), 500
    

@app.route('/')
def index():
    return render_template("tt.html")
@app.route('/api/print-requests', methods=['POST'])
def create_print_request():
    name = request.form.get('name')
    users = json.loads(request.form.get('users'))  # Get user object
    printer_owners = json.loads(request.form.get('printerOwners'))  # Get printer owner object
    
    documents = []
    
    for i, file in enumerate(request.files.getlist('documentFile[]')):
        document_name = request.form.getlist('documentName[]')[i]
        document_type = request.form.getlist('documentPrintType[]')[i]
        
        # Upload document to Azure Blob Storage
        document_url = upload_document_to_blob(file)
        
        documents.append({
            "documentName": document_name,
            "documentUrl": document_url,
            "documentPrintType": document_type
        })
    
    # Build the print request object
    print_request = {
        "name": name,
        "users": users,
        "printerOwners": printer_owners,
        "PrintsRequestStatus": False,
        "documentsAssigned": documents
    }
    
    # Simulate saving the print request (in a database or further processing)
    print(f"Print request created: {print_request}")
    
    # Return the print request as a response (replace with real ID after saving in DB)
    return jsonify({"id": "123", "message": "Print request created successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
