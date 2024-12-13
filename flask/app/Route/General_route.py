from flask import Blueprint, Response,  request,  render_template, session,flash,redirect,url_for
import requests
from app.DB.Db_config import USER_collection,PrintOwner_collection,PrintRequest_collection
from bson import ObjectId
from app.function import current_user, login_required, serialize
general_bp = Blueprint('general_bp', __name__)






@general_bp.route('/')
@login_required
def index():
    if session['user_role']=="USER":
        return redirect(url_for("puser_bp.get_all"))
    return render_template("home/index.html",segment="index",user=current_user())

@general_bp.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user exists in the User or PrinterOwner table
        user = USER_collection.find_one({"email":email}) or PrintOwner_collection.find_one({"email":email})

        if user and user["password"]== password:
            print(user)
            print(session)
            session.clear()
            # Store user session info (e.g., user ID)
            session['user_id'] = str(user['_id'])
            session["user_role"]=user['role']
            user['_id'] = str(user['_id'])
            session['user'] = user
            if user['role']=="USER":
                flash('Logged in successfully!', 'success')
                return redirect(url_for('puser_bp.get_all'))
            flash('Logged in successfully!', 'success')
            return redirect(url_for('general_bp.index'))  # Change 'dashboard' to your home route
        else:
            flash('Invalid email or password.', 'danger')
            return render_template("accounts/login.html")
        
        
        
    else:
        return render_template("accounts/login.html")


@general_bp.route('/signup')
def signup():
    return render_template("accounts/user_reg.html")
    
@general_bp.route('/logout')
def logout():
    session.clear()  # Clears all session data
    return redirect(url_for('general_bp.login'))



@general_bp.route("/selectprinter/<string:printer_id>")
def select_printer(printer_id):
    session['printer_id']=printer_id
    return redirect(url_for("print_req_bp.create_print_request"))



@general_bp.route("/update_user_session")
def update_user_session():
    user=current_user()
    user['_id'] = str(user['_id'])
    try:
        user["print_requests"]=[str(id_)for id_ in user['print_requests']]
    except:
        user["print_requests"]=0
    return user


@general_bp.route("/all-requests")
@login_required
def all_requests():
    return render_template("home/requests.html",user=current_user())

@general_bp.route("/requests-detail/<string:_id>")
@login_required
def requests_detail(_id):
    user=PrintRequest_collection.find_one({"_id":_id})
    user = serialize(user)
    print(user)
    return render_template("home/request-detail-page.html",request=user)

@general_bp.route('/print')
@login_required
def print_request():
   
    pdf_url = request.args.get("pdf")
    if not pdf_url:
        return "No PDF URL provided", 400
    
    response = requests.get(pdf_url)
    if response.status_code != 200:
        return "Failed to retrieve PDF", 404

    # Serve the PDF with appropriate headers
    return Response(response.content, mimetype='application/pdf',
                    headers={"Content-Disposition": "inline; filename=yourfile.pdf"})
    
    
    
@general_bp.route('/policies')
def policies():
    return render_template("home/policies-page.html",segment="policies")