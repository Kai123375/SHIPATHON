from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle, Color
from kivy.properties import ListProperty
from kivy.animation import Animation
import numpy as np

class GradientBox(BoxLayout):
    start_color = ListProperty([0.2, 0.4, 0.8, 1])
    end_color = ListProperty([0.6, 0.2, 0.8, 1])
    angle = ListProperty([0, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update, size=self.update)
        self.animate_gradient()

    def update(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.start_color)
            Rectangle(pos=self.pos, size=self.size)
            Color(rgba=self.end_color)
            Rectangle(
                pos=[self.pos[0] + self.angle[0] * self.size[0], 
                     self.pos[1] + self.angle[1] * self.size[1]],
                size=self.size
            )

    def animate_gradient(self):
        angle_seq = [
            [0, 1], [1, 1], [1, 0], [0, 0],
            [-1, 0], [-1, -1], [0, -1], [0, 0]
        ]
        anim = Animation(angle=angle_seq[0], duration=2)
        for angle in angle_seq[1:]:
            anim += Animation(angle=angle, duration=2)
        anim.repeat = True
        anim.start(self)