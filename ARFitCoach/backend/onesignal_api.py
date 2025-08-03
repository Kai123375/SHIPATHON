import requests
import os
from dotenv import load_dotenv

load_dotenv()

class OneSignalAPI:
    def __init__(self):
        self.app_id = os.getenv('ONESIGNAL_APP_ID')
        self.api_key = os.getenv('ONESIGNAL_API_KEY')

    def send_notification(self, player_ids, message, data=None):
        headers = {
            "Authorization": f"Basic {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "app_id": self.app_id,
            "include_player_ids": player_ids,
            "contents": {"en": message},
            "data": data or {},
            "ios_badgeType": "Increase",
            "ios_badgeCount": 1
        }

        response = requests.post(
            "https://onesignal.com/api/v1/notifications",
            headers=headers,
            json=payload
        )
        
        return response.json()

    def send_workout_reminder(self, player_id):
        return self.send_notification(
            [player_id],
            "Time for your daily workout! Keep your streak going!",
            {"screen": "workout"}
        )