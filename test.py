import requests

url = "https://api.hikerapi.com/a1/user/by/username"
params = {'username': 'wwe', 'access_key': 'lhj296a0Jh95iJyGs5cAIiA8Aq36AiU4'}
headers = {'accept': 'application/json'}

response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
    # Request was successful
    data = response.json()
    print(data)
else:
    # Request failed
    print(f"Error {response.status_code}: {response.text}")


from instagrapi import Client

cl=Client(session={'uuids': {'phone_id': 'aae9fba8-6e76-44ee-a4fd-7d7a5b390ebb', 'uuid': 'a3447d7a-46fe-4026-99ff-9d2e0ea5a621', 'client_session_id': '874af527-d6a3-4c99-b805-c2550d4e3853', 'advertising_id': '2b0e5dd0-b792-4438-ba7b-0e0816ac2060', 'android_device_id': 'android-5c8ccc88ad99b388', 'request_id': '4be3e6c4-3e2d-423d-b174-e033e85c45a3', 'tray_session_id': '2fa49c01-7334-481c-a3f6-4e029767489b'}, 'mid': 'ZeM7vQABAAGoRrzXTJb-RIBKKvXv', 'ig_u_rur': None, 'ig_www_claim': None, 'authorization_data': {'ds_user_id': '50648708396', 'sessionid': '50648708396%3AlOdexoEcm36mr8%3A9%3AAYdzCRMtE482KAkUmIJUmEl-qjbNvHWur5JZA5eOJA'}, 'cookies': {}, 'last_login': 1709390794.0164678, 'device_settings': {'app_version': '269.0.0.18.75', 'android_version': 26, 'android_release': '8.0.0', 'dpi': '480dpi', 'resolution': '1080x1920', 'manufacturer': 'OnePlus', 'device': 'devitron', 'model': '6T Dev', 'cpu': 'qcom', 'version_code': '314665256'}, 'user_agent': 'Instagram 269.0.0.18.75 Android (26/8.0.0; 480dpi; 1080x1920; OnePlus; 6T Dev; devitron; qcom; en_US; 314665256)', 'country': 'US', 'country_code': 1, 'locale': 'en_US', 'timezone_offset': -14400} )

print(cl.get_settings())

user_info=cl.user_id_from_username("Dheeraj_joshi2006")

print(user_info)