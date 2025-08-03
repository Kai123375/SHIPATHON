import requests
import os
from dotenv import load_dotenv

load_dotenv()

class RevenueCatAPI:
    def __init__(self):
        self.api_key = os.getenv('REVENUECAT_API_KEY')
        self.base_url = "https://api.revenuecat.com/v1"

    def check_subscription(self, user_id):
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.get(
            f"{self.base_url}/subscribers/{user_id}",
            headers=headers
        )
        return response.json().get('subscriber', {}).get('entitlements', {}).get('premium', {}).get('is_active', False)

    def grant_trial(self, user_id):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "entitlement": "premium",
            "platform": "kivy",
            "expiration_date": None  # Lifetime access for demo
        }
        response = requests.post(
            f"{self.base_url}/subscribers/{user_id}/entitlements",
            headers=headers,
            json=payload
        )
        return response.status_code == 200