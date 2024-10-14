import threading
from flask import Blueprint, flash, jsonify,request,redirect,render_template, session
from app.function import  selenium_task,login_required
from ..DB.Db_config import collection
import pandas as pd
from bson.objectid import ObjectId
from ..functions_modules.scouter.scouter_functions import Add_places_city_main

scouter_bp = Blueprint('scouter_bp', __name__,url_prefix="/scouter")

all_threads=[]
@scouter_bp.route('/add-city', methods=['GET', 'POST'])
@login_required
def Add_city():
    if request.method=="POST":
        print(request.form)
        global all_threads
        all_threads = [thread for thread in all_threads if thread["Thread"].is_alive()]
        action=request.form.get('cityID')
        cityID = request.form.get('cityID')
        country = request.form.get('country')
        tags = request.form.getlist('tags[]')

        # Handle the form data here (e.g., save to a database or process as needed)
        print(f"City ID: {cityID}")
        print(f"Country: {country}")
        print(f"Tags: {tags}")
        for t in all_threads:
            if t['Action'] == action and t['Thread'].name==session['user_id']+"_"+action and t['Thread'].is_alive():
                print("Thread is running.")
                print(all_threads)
                data={"status":"success","message":"thread already running  "}
                return render_template("scouter-pages/add-city.html", message=data,segment="auto_text")
        th = threading.Thread(target=Add_places_city_main, args=(cityID,country,tags), name=session['user_id']+"_"+action)
        all_threads.append({"Action": action, "Thread": th})
        th.start()
        print("Thread is not running. Creating a new thread.")
        print(all_threads)
        data={"status":"success","message":"Auto text started , Check your phone for the otp and verify it  "}
        return render_template('scouter-pages/add-city.html', message=data,segment="auto_text")
    
    return render_template("scouter-pages/add-city.html",segment="add-city" )