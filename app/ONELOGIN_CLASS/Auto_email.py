from app.DB.Db_config import collection
from bson import ObjectId
from app.ONELOGIN_CLASS.ONELOGIN import onLogin
from app.function import send_email


def auto_email_via_html(all_urls,email_subject,email_body,user_id):
    user_id = ObjectId(str(user_id))
    user = collection.find_one({"_id": user_id})
    object=onLogin()
    object.login_to_oneLogin()
    object.open_eleads_oneLogin()
    print("this is done now moving to all urls")
    print(all_urls)
    send_email("Update From Tikun-Automation","Hi your Automatic Emails process is starting now will inform you when it's finished ")

    for url in all_urls:
        print("i am for loop ")
        try:
            object.send_email_via_html(url,email_subject,email_body)
            user["todays_emails"] = user.get("todays_emails", 0) + 1
            result = collection.update_one({"_id": user_id}, {"$set": user})
        except Exception as err:
            print(err)
            pass
    send_email("Update From Tikun-Automation","Hi your Automatic Emails process is Completed  now ")
def auto_email_via_text(all_urls,email_subject,email_body,user_id):
    user_id = ObjectId(str(user_id))
    user = collection.find_one({"_id": user_id})
    object=onLogin()
    object.login_to_oneLogin()
    object.open_eleads_oneLogin()
    print("this is done now moving to all urls")
    print(all_urls)
    send_email("Update From Tikun-Automation","Hi your Automatic Emails process is starting now will inform you when it's finished ")

    for url in all_urls:
        print("i am for loop ")
        try:
            object.send_email_via_text(url,email_subject,email_body)
            user["todays_emails"] = user.get("todays_emails", 0) + 1
            result = collection.update_one({"_id": user_id}, {"$set": user})
        except Exception as err:
            print(err)
            pass
    send_email("Update From Tikun-Automation","Hi your Automatic Emails process is Completed  now ")



