from kivy.uix.button import Button
from kivy.properties import ListProperty, NumericProperty
from kivy.animation import Animation

class HoverButton(Button):
    hover_color = ListProperty([0.2, 0.5, 0.8, 1])
    normal_color = ListProperty([0.1, 0.3, 0.6, 1])
    shadow_radius = NumericProperty(10)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = self.normal_color
        self.bind(on_enter=self.animate_hover, on_leave=self.animate_normal)

    def animate_hover(self, *args):
        anim = Animation(
            background_color=self.hover_color,
            shadow_radius=15,
            duration=0.2
        )
        anim.start(self)

    def animate_normal(self, *args):
        anim = Animation(
            background_color=self.normal_color,
            shadow_radius=10,
            duration=0.2
        )
        anim.start(self)