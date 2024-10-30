from flask import Blueprint,  flash,  redirect, render_template, request, jsonify, session, url_for
from bson import ObjectId
import os
from PyPDF2 import PdfReader
from app.DB.Db_config import USER_collection,PrintOwner_collection,PrintRequest_collection
from app.Model.Print_req_model import PrintsRequests
print_req_bp = Blueprint('print_req_bp', __name__)


from app.function import current_user, upload_document_to_blob, user_by_id



@print_req_bp.route('/create_print_request', methods=['GET','POST'])
def create_print_request():
    if request.method=="POST":
        name = request.form.get('name')
        
        users = current_user()
        printer_owners = user_by_id(session['printer_id'])  # Get printer owner object
        
        documents = []
        user_total_request_price=0
        printer_total_request_price=0
        
        for i, file in enumerate(request.files.getlist('documentFile[]')):
            document_name = file.filename
            document_quantity = request.form.getlist('documentQuantity[]')[i]
            document_type = request.form.getlist('documentPrintType[]')[i]
            
            # Upload document to Azure Blob Storage
            document_url = upload_document_to_blob(file)
            
            if file.filename.lower().endswith('.pdf'):
                reader = PdfReader(file)
                total_pages = len(reader.pages)
            else:
                total_pages = 1  # Default for non-PDF files or if you don't need to calculate
            if document_type=="colored":
                price=11*int(total_pages)*int(document_quantity)
                user_total_request_price+=price
                
                pprice=10*int(total_pages)*int(document_quantity)
                printer_total_request_price+=pprice
            else:
                price=2.5*int(total_pages)*int(document_quantity)
                user_total_request_price+=price
                pprice=2*int(total_pages)*int(document_quantity)
                printer_total_request_price+=pprice
                
            documents.append({
                "documentName": document_name,
                "documentUrl": document_url,
                "documentPrintQuantity": document_quantity,
                "documentPrintType": document_type,
                "totalPages": total_pages,
                "Ucost":price,
                "Pcost":pprice
            })
        print_request_data = {
            "name": name,
            "users": users,
            "printerOwners": printer_owners,
            "PrintsRequestStatus": False,
            "documentsAssigned": documents,
            "documentPrintCostU":user_total_request_price,
            "documentPrintCostP":printer_total_request_price
        }

        # Insert the print request into the collection
        recoard = PrintRequest_collection.insert_one(print_request_data)
        print_request_id = recoard.inserted_id

        # Update the user document to append the new print request ID
        USER_collection.update_one(
            {"_id": ObjectId(users["_id"])},  # Assuming users is a dict with an _id field
            {"$addToSet": {"print_requests": print_request_id}}
        )
        try:
            printer_credits=printer_owners['printer_credits']
            total_credits=printer_owners['printer_total_credits'] 
        except:
            printer_credits=0
            total_credits=0
            
        # Update the printer owner document to append the new print request ID
        PrintOwner_collection.update_one(
                {"_id": ObjectId(printer_owners["_id"])},  # Filter criteria
                {
                    "$addToSet": {"print_requests": print_request_id},  # Add print request
                    "$set": {
                        "printer_credits": printer_credits + printer_total_request_price,
                        "printer_total_credits": total_credits + printer_total_request_price
                    }
                },
                upsert=True  # Upsert option
            )

        # Simulate saving the print request (in a database or further processing)
        print(f"Print request created: {print_request_data}")
        flash("Print Requested Successfully","success")
        return redirect(url_for("general_bp.index"))
    else:
        return render_template("home/printREQUEST.html", user=current_user())
    
    
@print_req_bp.route('/update_print_request/<string:request_id>')
def update_print_request(request_id):
    try:
        # Parse JSON data from the request body
        update_data = {"PrintsRequestStatus":True}

        # Validate incoming data with PrintsRequests schema (if needed)
        schema = PrintsRequests()
        errors = schema.validate(update_data)
        if errors:
            return jsonify({"errors": errors}), 400

        # Convert request_id to ObjectId (for MongoDB compatibility)
        object_id = ObjectId(request_id)

        # Update the record in MongoDB
        result =PrintRequest_collection.update_one(
            {"_id": object_id},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            return jsonify({"error": "Print request not found"}), 404

        return redirect(url_for('general_bp.all_requests'))

    except Exception as e:
        return jsonify({"error": str(e)}), 500