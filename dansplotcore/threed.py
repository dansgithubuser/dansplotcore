from . import media

import numpy as np

import math

vert_shader_src = b'''\
uniform vec2 uOrigin;
uniform vec2 uZoom;
uniform vec2 uSlice;

attribute vec3 aPosition;
attribute vec4 aColor;

varying vec4 vColor;

void main() {
    gl_Position = vec4(
        (aPosition.x - uOrigin.x) * uZoom.x,
        (aPosition.y - uOrigin.y) * uZoom.y,
        0.0,
        1.0
    );
    float view_distance = aPosition.z;
    if (uSlice[0] <= view_distance && view_distance <= uSlice[1]) {
        vColor = aColor;
    } else {
        vColor = vec4(aColor.rgb, 0.0);
    }
}
'''

frag_shader_src = b'''\
varying vec4 vColor;

void main() {
    gl_FragColor = vColor;
}
'''

class Plot:
    def __init__(
        self,
        title='plot',
    ):
        self.title = title
        self.points = media.Buffer3d()
        self.tris = media.Buffer3d()
        self.x_min = +math.inf
        self.x_max = -math.inf
        self.y_min = +math.inf
        self.y_max = -math.inf
        self.z_min = +math.inf
        self.z_max = -math.inf

    def point(self, x, y, z, r, g, b, a):
        self.points.add(x, y, z, r, g, b, a)
        self.include(x, y, z)

    def triangle(self, xa, ya, za, xb, yb, zb, xc, yc, zc, r, g, b, a):
        self.tris.add(xa, ya, za, r, g, b, a)
        self.tris.add(xb, yb, zb, r, g, b, a)
        self.tris.add(xc, yc, zc, r, g, b, a)
        self.include(xa, ya, za)
        self.include(xb, yb, zb)
        self.include(xc, yc, zc)

    def grid_cube(self, x, y, z, half_edge, r, g, b, a):
        xi = x - half_edge / 2
        yi = y - half_edge / 2
        zi = z - half_edge / 2
        xf = x + half_edge / 2
        yf = y + half_edge / 2
        zf = z + half_edge / 2
        self.triangle(xi, yi, zi, xf, yi, zi, xf, yf, zi, r, g, b, a)
        self.triangle(xi, yi, zi, xi, yf, zi, xf, yf, zi, r, g, b, a)
        self.triangle(xi, yi, zi, xi, yf, zi, xi, yf, zf, r, g, b, a)
        self.triangle(xi, yi, zi, xi, yi, zf, xi, yf, zf, r, g, b, a)
        self.triangle(xi, yi, zi, xf, yi, zi, xf, yi, zf, r, g, b, a)
        self.triangle(xi, yi, zi, xi, yi, zf, xf, yi, zf, r, g, b, a)
        self.triangle(xf, yf, zf, xi, yf, zf, xi, yi, zf, r, g, b, a)
        self.triangle(xf, yf, zf, xf, yi, zf, xi, yi, zf, r, g, b, a)
        self.triangle(xf, yf, zf, xf, yi, zf, xf, yi, zi, r, g, b, a)
        self.triangle(xf, yf, zf, xf, yf, zi, xf, yi, zi, r, g, b, a)
        self.triangle(xf, yf, zf, xi, yf, zf, xi, yf, zi, r, g, b, a)
        self.triangle(xf, yf, zf, xf, yf, zi, xi, yf, zi, r, g, b, a)

    def include(self, x, y, z):
        self.x_min = min(x, self.x_min)
        self.x_max = max(x, self.x_max)
        self.y_min = min(y, self.y_min)
        self.y_max = max(y, self.y_max)
        self.z_min = min(z, self.z_min)
        self.z_max = max(z, self.z_max)

    def show(self, w=640, h=480):
        class U: pass
        class State:
            shift = False
            ctrl = False
        media.init(
            w,
            h,
            self.title,
            program=(
                vert_shader_src,
                frag_shader_src,
                ['uOrigin', 'uZoom', 'uSlice'],
                ['aPosition', 'aColor'],
            ),
        )
        def reset():
            x = self.x_min
            y = self.y_min
            w = self.x_max - self.x_min
            h = self.y_max - self.y_min
            if x == math.inf:
                x = 0
                y = 0
                w = 1
                h = 1
            if w == 0:
                w = 1
            if h == 0:
                h = 1
            U.origin = [x + w/2, y + h/2]
            U.zoom = [2/w, 2/h]
            U.slice = [self.z_min, self.z_max]
        reset()
        # construct
        self.points.prep('static')
        self.points.draws = [('points', 0, len(self.points))]
        self.tris.prep('static')
        self.tris.draws = [('triangles', 0, len(self.tris))]
        # callbacks
        def key_press(key):
            if key in ['LShift', 'RShift']:
                State.shift = True
            elif key in ['LCtrl', 'RCtrl']:
                State.ctrl = True
        def key_release(key):
            if key in ['LShift', 'RShift']:
                State.shift = False
            elif key in ['LCtrl', 'RCtrl']:
                State.ctrl = False
        def mouse_scroll(x, y, delta):
            if State.shift and not State.ctrl:
                d = U.slice[1] - U.slice[0]
                if delta > 0: d *= -1
                U.slice[0] += d / 4
                U.slice[1] += d / 4
            elif State.shift and State.ctrl:
                m = sum(U.slice) / 2
                d = U.slice[1] - m
                if delta < 0:
                    d *= 1.25
                else:
                    d *= 0.8
                U.slice[0] = m - d
                U.slice[1] = m + d
        def draw():
            media.clear()
            media.gl.glUniform2f(media.F.locations['uOrigin'], *U.origin)
            media.gl.glUniform2f(media.F.locations['uZoom'  ], *U.zoom)
            media.gl.glUniform2f(media.F.locations['uSlice' ], *U.slice)
            self.points.draw()
            self.tris.draw()
        media.set_callbacks(
            mouse_scroll=mouse_scroll,
            key_press=key_press,
            key_release=key_release,
            draw=draw,
        )
        # run
        media.run()
