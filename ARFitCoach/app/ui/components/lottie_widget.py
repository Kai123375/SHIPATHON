from kivy.uix.widget import Widget
from kivy.properties import (StringProperty, NumericProperty, 
                           ListProperty, BooleanProperty, ObjectProperty)
from kivy.graphics import Rectangle, Color, RoundedRectangle
from kivy.graphics.texture import Texture  # <-- Missing import added
from kivy.clock import Clock, mainthread
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.logger import Logger
import json
import io
import threading

Builder.load_string('''
<EnhancedLottie>:
    canvas.before:
        Color:
            rgba: root.background_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(10),]
''')

class EnhancedLottie(Widget):
    source = StringProperty()
    frame_rate = NumericProperty(30)
    background_color = ListProperty([0.1, 0.1, 0.1, 1])
    auto_play = BooleanProperty(True)
    loop = BooleanProperty(True)
    texture = ObjectProperty(None, allownone=True)  # <-- Proper texture property
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._frames = []
        self._current_frame = 0
        self._load_thread = None
        self.bind(
            source=self._on_source,
            size=self._update_texture,
            pos=self._update_texture
        )

    def _on_source(self, instance, value):
        if value:
            self._stop_loading()
            self._load_thread = threading.Thread(
                target=self._load_animation,
                daemon=True
            )
            self._load_thread.start()

    def _stop_loading(self):
        if self._load_thread and self._load_thread.is_alive():
            self._load_thread.join(timeout=0.1)

    def _load_animation(self):
        try:
            with open(self.source) as f:
                data = json.load(f)
            self._frames = self._parse_frames(data)
            self._trigger_texture_update()
        except Exception as e:
            Logger.error(f"LottieWidget: {str(e)}")
            self._frames = self._create_placeholder()

    def _parse_frames(self, data):
        """Parse animation frames - implement actual Lottie rendering here"""
        return [(i, None) for i in range(60)]  # Placeholder

    def _create_placeholder(self):
        """Create fallback frames when loading fails"""
        return [(0, None)]

    @mainthread
    def _trigger_texture_update(self):
        if self.auto_play:
            self.play()

    def play(self):
        Clock.unschedule(self._next_frame)
        Clock.schedule_interval(self._next_frame, 1 / max(1, self.frame_rate))

    def pause(self):
        Clock.unschedule(self._next_frame)

    def stop(self):
        self.pause()
        self._current_frame = 0
        self._update_texture()

    def _next_frame(self, dt):
        if not self._frames:
            return
            
        self._current_frame = (self._current_frame + 1) % len(self._frames)
        self._update_texture()

    def _update_texture(self, *args):
        if not self._frames or not 0 <= self._current_frame < len(self._frames):
            return

        # Create or update texture
        if not self.texture:
            self.texture = Texture.create(size=(dp(256), dp(256)))
        
        # Actual rendering would happen here
        self._render_current_frame()

    def _render_current_frame(self):
        """Replace with actual frame rendering logic"""
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(
                texture=self.texture,
                pos=self.pos,
                size=self.size
            )

    def reload(self):
        """Force reload the animation"""
        self._on_source(None, self.source)