import requests
import os
from dotenv import load_dotenv
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy.lang import Builder

load_dotenv()

Builder.load_string('''
<PaywallScreen>:
    size_hint: (0.9, 0.8)
    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        Label:
            text: 'Go Premium'
            font_size: '24sp'
            bold: True
        Button:
            text: 'Monthly ($9.99)'
            on_press: root.purchase('monthly')
        Button:
            text: 'Annual ($49.99)'
            on_press: root.purchase('annual')
        Button:
            text: 'Close'
            on_press: root.dismiss()
''')

class RevenueCatManager:
    def __init__(self):
        self.api_key = os.getenv('REVENUECAT_API_KEY')
        self.base_url = "https://api.revenuecat.com/v1"

    def get_subscription_status(self, user_id):
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.get(
            f"{self.base_url}/subscribers/{user_id}",
            headers=headers
        )
        return response.json()

    def grant_entitlement(self, user_id, product_id):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "entitlement": "premium",
            "platform": "kivy",
            "product_id": product_id
        }
        response = requests.post(
            f"{self.base_url}/subscribers/{user_id}/entitlements",
            headers=headers,
            json=payload
        )
        return response.status_code == 200

class PaywallScreen(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rc = RevenueCatManager()

    def purchase(self, plan_type):
        product_id = {
            'monthly': 'premium_monthly',
            'annual': 'premium_annual'
        }.get(plan_type)
        
        if self.rc.grant_entitlement("user123", product_id):
            self.dismiss()