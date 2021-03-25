import pyrebase

import firebase_admin
from firebase_admin import credentials, auth as admin_auth



cred = credentials.Certificate(
    "/path/to/credentials.json")
firebase_admin.initialize_app(cred)

config = {
    #Enter your config here
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()
storage = firebase.storage()


def check_user_authenticity(session_id):
    decoded_token = admin_auth.verify_id_token(session_id)
    uid = decoded_token['uid']
    print(uid)
    return True if uid else False