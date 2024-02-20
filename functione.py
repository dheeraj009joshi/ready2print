import time
from functools import wraps
from flask import session,redirect,url_for,request, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId
from selenium import webdriver
from app.DB.Db_config import collection
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session and 'username' in session:
            return func(*args, **kwargs)
        else:
            # Store the requested URL in the session before redirecting to login
            session['next_url'] = request.url
            return redirect(url_for('general_bp.login'))
    return wrapper
    
def onelogin_login():
    time.sleep(10)
    for i in range(23):
        print(i)
        time.sleep(1)
        
    return True

def selenium_task():
    global selenium_status
    try:
        # Update status - script started

        # Create a new WebDriver instance
        driver = webdriver.Chrome()  # Adjust the path to your chromedriver executable

        try:
            # Perform Selenium actions here
            driver.get('https://www.google.com')
            time.sleep(100)
            selenium_status = {'message': 'Search performed', 'progress': 100}
          

        finally:
            # Close the WebDriver instance to avoid resource leaks
            driver.quit()

    except Exception as e:
        # Handle exceptions and update status accordingly
        selenium_status = {'message': f'Selenium script failed: {str(e)}', 'progress': 100}
        
        
def current_user():
    # Check if the user is logged in
    if 'user_id' in session:
        user_id = session['user_id']

        # Retrieve user data from MongoDB using the user_id
        user_data = collection.find_one({'_id': ObjectId(user_id)})

        return user_data