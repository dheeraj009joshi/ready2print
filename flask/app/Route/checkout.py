from flask import Blueprint, Response,  request,  render_template, session,flash,redirect,url_for
import requests
from app.DB.Db_config import USER_collection,PrintOwner_collection,PrintRequest_collection
from bson import ObjectId
from app.function import current_user, login_required, serialize
checkout_bp = Blueprint('checkout_bp', __name__)






@checkout_bp.route('/checkout')
@login_required
def index():
    print_request=PrintRequest_collection.find_one({"_id":request.args.get("print_request_id")})
    print(print_request)
    return render_template("home/checkout-page.html",segment="index",user=current_user(),request=print_request)