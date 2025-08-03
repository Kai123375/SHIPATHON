import os
import sys
from pathlib import Path
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.utils import get_color_from_hex as hex

# Fix Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import backend modules with error handling
try:
    from backend.firebase_db import FirebaseManager
    from backend.revenuecat_api import RevenueCatAPI
except ImportError as e:
    print(f"Backend import error: {e}")
    # Fallback implementations
    class FirebaseManager:
        def __init__(self): print("Dummy FirebaseManager created")
        def save_workout(self, *args): print("Dummy save_workout called")
        def get_leaderboard(self): return []
    class RevenueCatAPI:
        def __init__(self): print("Dummy RevenueCatAPI created")
        def check_subscription(self, user_id): return False
        def grant_trial(self, user_id): return True

Window.size = (414, 896)  # iPhone-style dimensions

class GradientMixin:
    colors = ListProperty(['#1E293B', '#0F172A'])
    angle = NumericProperty(45)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._update_gradient, size=self._update_gradient)
    
    def _update_gradient(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            # Top color
            Color(rgba=self.hex_to_rgba(self.colors[0]))
            Rectangle(pos=self.pos, size=self.size)
            # Bottom color
            Color(rgba=self.hex_to_rgba(self.colors[1]))
            Rectangle(
                pos=(self.x, self.y),
                size=(self.width, self.height/2)
            )
    
    def hex_to_rgba(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return [int(hex_color[i:i+2], 16)/255.0 for i in (0, 2, 4)] + [1.0]

class WorkoutScreen(Screen, GradientMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.colors = ['#1E293B', '#0F172A']
    
    def on_enter(self):
        if hasattr(self, 'ids'):
            Animation(opacity=1, duration=0.3).start(self.ids.get('workout_area', None))

class PaywallScreen(Screen, GradientMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.colors = ['#0F172A', '#1E293B']  # Reversed gradient
    
    def on_enter(self):
        if hasattr(self, 'children'):
            for child in self.children[0].children[:-1]:
                child.opacity = 0
                Animation(opacity=1, duration=0.2).start(child)

Builder.load_string('''
#:import hex kivy.utils.get_color_from_hex
#:import FadeTransition kivy.uix.screenmanager.FadeTransition

<GlassButton@Button>:
    background_normal: ''
    background_color: (0,0,0,0)
    color: hex('#FFFFFF')
    font_size: dp(16)
    canvas.before:
        Color:
            rgba: hex('#FFFFFF10') if self.state == 'normal' else hex('#FFFFFF20')
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [dp(12),]
        Line:
            rounded_rectangle: [self.x, self.y, self.width, self.height, dp(12)]
            width: dp(1.5)
            color: hex('#FFFFFF60')

<WorkoutScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        
        Label:
            text: 'WORKOUT MODE'
            font_size: dp(24)
            color: hex('#FFFFFF')
            size_hint_y: None
            height: dp(50)
        
        BoxLayout:
            id: workout_area
            size_hint_y: 0.7
        
        GlassButton:
            text: 'PREMIUM'
            on_press: root.manager.transition = FadeTransition(); root.manager.current = 'paywall'
            color: hex('#F59E0B')
            size_hint_y: None
            height: dp(50)

<PaywallScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(30)
        spacing: dp(25)
        
        Label:
            text: 'UNLOCK PREMIUM'
            font_size: dp(28)
            color: hex('#FFFFFF')
            size_hint_y: None
            height: dp(50)
        
        BoxLayout:
            orientation: 'vertical'
            spacing: dp(15)
            
            GlassButton:
                text: 'MONTHLY \\n$9.99/month'
                font_size: dp(18)
                background_color: hex('#F59E0B80')
            
            GlassButton:
                text: 'ANNUAL \\n$49.99/year'
                font_size: dp(18)
                background_color: hex('#10B98180')
            
            GlassButton:
                text: 'BACK'
                on_press: root.manager.transition = FadeTransition(); root.manager.current = 'workout'
                color: hex('#94A3B8')
                size_hint_y: None
                height: dp(40)
''')

class ARFitCoachApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.firebase = FirebaseManager()
        self.revenuecat = RevenueCatAPI()
        
    def build(self):
        self.sm = ScreenManager(transition=FadeTransition())
        self.sm.add_widget(WorkoutScreen(name='workout'))
        self.sm.add_widget(PaywallScreen(name='paywall'))
        return self.sm

if __name__ == '__main__':
    ARFitCoachApp().run()