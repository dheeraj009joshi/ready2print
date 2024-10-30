from bson import ObjectId
from flask import Blueprint, flash, jsonify, render_template,request,redirect, url_for
from ..Model.Printer_owner_model import PrinterOwnerSchema
from ..DB.Db_config import PrintOwner_collection,PrintRequest_collection
from ..function import current_user
puser_bp = Blueprint('puser_bp', __name__)


@puser_bp.route('/Pusers', methods=['POST'])
def create_user():
    try:
        
        email = request.form['email']
        if PrintOwner_collection.find_one({"email":email}):
            flash('Email already exists. Please use a different email.', 'danger')
            return redirect(url_for('general_bp.signup'))
        else:
            user_data = request.form
            user_schema = PrinterOwnerSchema()
            result = user_schema.load(user_data)
            inserted_user = PrintOwner_collection.insert_one(result).inserted_id
            print( jsonify({'status': 'success', 'message': 'User added successfully', 'user_id': str(inserted_user)}))
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('general_bp.login'))
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400



@puser_bp.route('/allPusers', methods=['GET'])
def get_all():
    data = PrintOwner_collection.find({})
    printers = []
    
    for printer in data:
        # Convert MongoDB ObjectId to string and include other fields as needed
        printer['_id'] = str(printer['_id'])  # Convert ObjectId to string
        printers.append(printer)
        try:
            printer_request_ids = [ObjectId(id_) for id_ in  printer['print_requests']]
            print(printer_request_ids)
            printer_requests = list(PrintRequest_collection.find({"_id": {"$in": printer_request_ids}}))
            print(printer_requests)
            # Filter for pending requests
            pending_requests = [req for req in printer_requests if req['PrintsRequestStatus'] == False]
            printer['pending_requests_count'] = len(pending_requests)
        except:
            printer['pending_requests_count']=0
        

    print(printers)
    return render_template("home/index.html",printers= printers,user=current_user())



