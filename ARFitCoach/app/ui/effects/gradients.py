from kivy.graphics import RenderContext, Rectangle
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, NumericProperty

class GradientEffect(Widget):
    colors = ListProperty(['#1E293B', '#0F172A'])
    angle = NumericProperty(45)

    def __init__(self, **kwargs):
        self.canvas = RenderContext()
        super().__init__(**kwargs)
        self.shader_source = '''
        $HEADER$
        uniform vec2 resolution;
        uniform float angle;
        uniform vec4 colors[2];

        void main(void) {
            vec2 uv = frag_coord.xy / resolution.xy;
            float a = radians(angle);
            float t = cos(a) * uv.x + sin(a) * uv.y;
            gl_FragColor = mix(colors[0], colors[1], t);
        }
        '''
        self.canvas.shader.fs = self.shader_source
        self.bind(pos=self.update, size=self.update)

    def update(self, *args):
        self.canvas['resolution'] = [float(v) for v in self.size]
        self.canvas['angle'] = float(self.angle)
        self.canvas['colors'] = [
            [float(c) for c in self.hex_to_rgba(self.colors[0])],
            [float(c) for c in self.hex_to_rgba(self.colors[1])]
        ]
        with self.canvas:
            Rectangle(pos=self.pos, size=self.size)

    def hex_to_rgba(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return [
            int(hex_color[i:i+2], 16)/255.0 
            for i in (0, 2, 4)
        ] + [1.0]