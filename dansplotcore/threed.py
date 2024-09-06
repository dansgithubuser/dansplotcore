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

class View:
    def __init__(self, x=None, y=None, w=None, h=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def tuple(self): return [self.x, self.y, self.w, self.h]

class Plot:
    def __init__(
        self,
        title='plot',
        *,
        hide_axes=False,
        x_axis_title=None,
        y_axis_title=None,
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
        self.hide_axes = hide_axes
        self.x_axis_title = x_axis_title
        self.y_axis_title = y_axis_title

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

    def grid_cube(self, x, y, z, edge, r, g, b, a):
        xi = x - edge / 2
        yi = y - edge / 2
        zi = z - edge / 2
        xf = x + edge / 2
        yf = y + edge / 2
        zf = z + edge / 2
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

    def clear(self):
        self.points.clear()
        self.tris.clear()

    def include(self, x, y, z):
        self.x_min = min(x, self.x_min)
        self.x_max = max(x, self.x_max)
        self.y_min = min(y, self.y_min)
        self.y_max = max(y, self.y_max)
        self.z_min = min(z, self.z_min)
        self.z_max = max(z, self.z_max)

    def show(self, w=640, h=480, *, update=None):
        class U: pass
        class State:
            shift = False
            ctrl = False
        view = View()
        buffer_dyn = media.Buffer3d()
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
            view.x = self.x_min
            view.y = self.y_min
            view.w = self.x_max - self.x_min
            view.h = self.y_max - self.y_min
            if view.x == math.inf:
                view.x = 0
                view.y = 0
                view.w = 1
                view.h = 1
            if view.w == 0:
                view.w = 1
            if view.h == 0:
                view.h = 1
            U.origin = [view.x + view.w/2, view.y + view.h/2]
            U.zoom = [2/view.w, 2/view.h]
            U.slice = [self.z_min, self.z_max]
        reset()
        # initial construct
        self.points.draws = [('points', 0, len(self.points))]
        self.tris.draws = [('triangles', 0, len(self.tris))]
        def construct():
            self.points.prep('static')
            self.tris.prep('static')
        construct()
        # callbacks
        def key_press(key):
            if key in ['LShift', 'RShift']:
                State.shift = True
            elif key in ['LCtrl', 'RCtrl']:
                State.ctrl = True
            elif key == ' ':
                reset()
            elif key == 'Return':
                media.capture()
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
        def draw_axes(texter):
            text_w = 10 / media.width()  * view.w
            text_h = 15 / media.height() * view.h
            margin_x = 5.0 / media.width()  * view.w
            margin_y = 5.0 / media.height() * view.h
            # draw x axis
            increment = 10 ** math.floor(math.log10(view.w))
            if view.w / increment < 2:
                increment /= 5
            elif view.w / increment < 5:
                increment /= 2
            i = view.x // increment * increment + increment
            if self.x_axis_title:
                x_axis_title_w = text_w * len(self.x_axis_title)
            else:
                x_axis_title_w = 0
            while i < view.x + view.w - (x_axis_title_w + 6 * text_w + margin_x):
                t = i
                s = '{:.5}'.format(t)
                texter.text(s, x=i+margin_x, y=view.y+margin_y, w=text_w, h=text_h)
                texter.text('L', i, view.y, text_w * 2, text_h)
                i += increment
            if self.x_axis_title:
                texter.text(
                    self.x_axis_title,
                    x=view.x + view.w - x_axis_title_w,
                    y=view.y + margin_y,
                    w=text_w,
                    h=text_h,
                )
            # draw y axis
            increment = 10 ** math.floor(math.log10(view.h))
            if view.h / increment < 2:
                increment /= 5
            elif view.h / increment < 5:
                increment /= 2
            i = (view.y + text_h + 2*margin_y) // increment * increment + increment
            if self.y_axis_title:
                y_axis_title_h = text_h + 2 * margin_y
            else:
                y_axis_title_h = 0
            while i < view.y + view.h - (text_h + 2 * margin_y + y_axis_title_h):
                t = i
                s = '{:.5}'.format(t)
                texter.text(s, x=view.x+margin_x, y=i+margin_y, w=text_w, h=text_h)
                texter.text('L', view.x, i, text_w * 2, text_h)
                i += increment
            if self.y_axis_title:
                texter.text(
                    self.y_axis_title,
                    x=view.x + margin_x,
                    y=view.y + view.h - text_h - margin_y,
                    w=text_w,
                    h=text_h,
                )
            # draw z axis
            texter.text(
                f'z = ({U.slice[0]:.3f}, {U.slice[1]:.3f})',
                x=view.x + view.w / 2,
                y=view.y + view.h - text_h - margin_y,
                w=text_w,
                h=text_h,
            )
        def draw():
            media.clear()
            media.gl.glUniform2f(media.F.locations['uOrigin'], *U.origin)
            media.gl.glUniform2f(media.F.locations['uZoom'  ], *U.zoom)
            media.gl.glUniform2f(media.F.locations['uSlice' ], *U.slice)
            texter = media.Texter()
            buffer_dyn.clear()
            if not self.hide_axes: draw_axes(texter)
            self.points.draw()
            self.tris.draw()
            buffer_dyn.add_data_2d_with_z(texter.data, z=(U.slice[0] + U.slice[1]) / 2)
            buffer_dyn.prep('dynamic')
            buffer_dyn.draws = [('lines', 0, len(buffer_dyn.data))]
            buffer_dyn.draw()
        media.set_callbacks(
            mouse_scroll=mouse_scroll,
            key_press=key_press,
            key_release=key_release,
            draw=draw,
        )
        if update:
            def wrap_update(dt):
                update(dt)
                construct()
        else:
            wrap_update = None
        # run
        media.run(update=wrap_update)
