from app.DB.Db_config import collection

from bson import ObjectId

from app.ONELOGIN_CLASS.ONELOGIN import onLogin
from app.function import send_email


def auto_text(all_urls, message,user_id):
    user_id = ObjectId(str(user_id))
    user = collection.find_one({"_id": user_id})
    object=onLogin()
    object.login_to_oneLogin()
    object.open_eleads_oneLogin()
    send_email("Update From Tikun-Automation","Hi your Automatic Message process is starting now will inform you when it's finished ")

    for url in all_urls:
        try:
            object.send_message(url,message)
            user["todays_emails"] = user.get("todays_emails", 0) + 1
            result = collection.update_one({"_id": user_id}, {"$set": user})
        except Exception as err:
            pass
    send_email("Update From Tikun-Automation","Hi your Automatic Message process is completed now ")