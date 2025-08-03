import firebase_admin
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv

load_dotenv()

class FirebaseManager:
    def __init__(self):
        # Complete service account configuration including required token_uri
        service_account_info = {
            "type": "service_account",
            "project_id": os.getenv('FIREBASE_PROJECT_ID'),
            "private_key": os.getenv('FIREBASE_KEY').replace('\\n', '\n'),
            "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
            "token_uri": "https://oauth2.googleapis.com/token",  # Required field
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{os.getenv('FIREBASE_CLIENT_EMAIL').replace('@', '%40')}"
        }
        
        try:
            cred = credentials.Certificate(service_account_info)
            firebase_admin.initialize_app(cred, {
                'databaseURL': os.getenv('FIREBASE_DB_URL')
            })
            self.ref = db.reference('/')
            print("Firebase initialized successfully")
        except Exception as e:
            print(f"Firebase initialization failed: {e}")
            raise

    def save_workout(self, user_id, exercise, metrics):
        if not hasattr(self, 'ref'):
            print("Firebase not initialized - skipping save")
            return
            
        workout_ref = self.ref.child('users').child(user_id).child('workouts')
        workout_ref.push({
            'exercise': exercise,
            'metrics': metrics,
            'timestamp': {'.sv': 'timestamp'}
        })

    def get_leaderboard(self):
        if not hasattr(self, 'ref'):
            print("Firebase not initialized - returning empty leaderboard")
            return []
        return self.ref.child('leaderboard').order_by_child('score').limit_to_last(10).get()