import moderngl as mgl
import moderngl_window as mglw
import numpy as np

import copy
import math

vertex_shader = '''\
#version 330

uniform vec2 u_origin;
uniform vec2 u_zoom;

in vec2 a_pos;
in vec4 a_color;

out vec4 v_color;

void main() {
    gl_Position = vec4(
        +(a_pos.x - u_origin.x) * u_zoom.x,
        -(a_pos.y - u_origin.y) * u_zoom.y,
        0.0,
        1.0
    );
    v_color = a_color;
}
'''

fragment_shader = '''\
#version 330

in vec4 v_color;

out vec4 o_color;

void main() {
    o_color = v_color;
}
'''

class Media:
    def view_set(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.u_origin.value = (x + w/2, y + h/2)
        self.u_zoom.value = (2/w, 2/h)

    def width(self):
        return self.w

    def height(self):
        return self.h

media = Media()

class View:
    def __init__(self, x=None, y=None, w=None, h=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def tuple(self): return [self.x, self.y, self.w, self.h]

def fcolor(r, g, b, a):
    return [
        i if type(i) == float else i/255
        for i in [r, g, b, a]
    ]

def construct(self, plot, view, w, h):
    verts = []
    # late vertexors
    if plot.late_vertexors:
        if hasattr(plot, 'original_points'):
            plot.points = copy.copy(plot.original_points)
            plot.lines = copy.copy(plot.original_lines)
        else:
            plot.original_points = copy.copy(plot.points)
            plot.original_lines = copy.copy(plot.lines)
        for i in plot.late_vertexors:
            i(view, w, h)
    # points
    for x, y, r, g, b, a in plot.points:
        verts.append([x, y, *fcolor(r, g, b, a)])
    points_f = len(verts)
    # lines
    for xi, yi, xf, yf, r, g, b, a in plot.lines:
        verts.append([xi, yi, *fcolor(r, g, b, a)])
        verts.append([xf, yf, *fcolor(r, g, b, a)])
    lines_f = len(verts)
    # rects
    for xi, yi, xf, yf, r, g, b, a in plot.rects:
        verts.append([xi, yi, *fcolor(r, g, b, a)])
        verts.append([xf, yf, *fcolor(r, g, b, a)])
        verts.append([xi, yf, *fcolor(r, g, b, a)])
        verts.append([xi, yi, *fcolor(r, g, b, a)])
        verts.append([xf, yf, *fcolor(r, g, b, a)])
        verts.append([xf, yi, *fcolor(r, g, b, a)])
    tris_f = len(verts)
    # draws
    self.va = self.ctx.vertex_array(
        self.prog,
        [(
            self.ctx.buffer(np.array(verts, dtype='f4')),
            '2f 4f',
            'a_pos',
            'a_color',
        )],
    )
    plot.verts = verts
    plot.draws = [
        ('TRIANGLES',  lines_f, tris_f   - lines_f ),
        ('LINES'    , points_f, lines_f  - points_f),
        ('POINTS'   ,        0, points_f - 0       ),
    ]

def show(plot, w, h):
    mouse = [0, 0]
    if plot.x_min == plot.x_max:
        plot.x_min -= 1
        plot.x_max += 1
    if plot.y_min == plot.y_max:
        plot.y_min -= 1
        plot.y_max += 1
    dx = plot.x_max - plot.x_min
    dy = plot.y_max - plot.y_min
    plot.x_min -= dx / 16
    plot.y_min -= dy / 16
    plot.x_max += dx / 16
    plot.y_max += dy / 16
    view = View()
    def reset():
        view.x = plot.x_min
        view.y = plot.y_min
        view.w = plot.x_max-plot.x_min
        view.h = plot.y_max-plot.y_min
        media.view_set(*view.tuple())
        plot.is_reset = True
    def move(view, dx, dy):
        view.x -= dx*view.w/media.width()
        view.y -= dy*view.h/media.height()
        media.view_set(*view.tuple())
        plot.is_reset = False
    def zoom(view, zx, zy, x, y):
        # change view so (x, y) stays put and (w, h) multiplies by (zx, zy)
        new_view_w = view.w*zx
        new_view_h = view.h*zy
        view.x += x/media.width () * (view.w - new_view_w)
        view.y += y/media.height() * (view.h - new_view_h)
        view.w = new_view_w
        view.h = new_view_h
        media.view_set(*view.tuple())
        plot.is_reset = False

    class Config(mglw.WindowConfig):
        gl_version = (3, 3)
        window_size = (w, h)

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.ctx.enable(mgl.BLEND)
            self.prog = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
            self.u_origin = self.prog['u_origin']
            self.u_origin.value = (0, 0)
            media.u_origin = self.u_origin
            self.u_zoom = self.prog['u_zoom']
            self.u_zoom.value = (1, 1)
            media.u_zoom = self.u_zoom
            construct(self, plot, view, w, h)
            self.data_static = self.ctx.vertex_array(
                self.prog,
                [(
                    self.ctx.buffer(np.array(plot.verts, dtype='f4')),
                    '2f 4f',
                    'a_pos',
                    'a_color',
                )],
            )
            reset()

        def resize(self, w, h):
            media.w = w
            media.h = h
            zoom(view, w/media.width(), h/media.height(), w/2, h/2)
            if plot.late_vertexors:
                construct(self, plot, view, media.width(), media.height())

        def mouse_position_event(self, x, y, dx, dy):
            mouse = x, y

        def mouse_drag_event(self, x, y, dx, dy):
            move(view, dx, dy)

        def mouse_scroll_event(self, x_offset, y_offset):
            z = 1.25 if y_offset > 0 else 0.8
            zoom(view, z, z, mouse[0], mouse[1])

        def key_event(self, key, action, modifiers):
            if action != self.wnd.keys.ACTION_PRESS: return
            #moves = {
            #    self.wnd.keys.LEFT : ( 10,   0),
            #    self.wnd.keys.RIGHT: (-10,   0),
            #    self.wnd.keys.UP   : (  0,  10),
            #    self.wnd.keys.DOWN : (  0, -10),
            #}
            #if key in moves:
            #    move(view, *moves[key])
            #    return
            #zooms = {
            #    self.wnd.keys.A: (1.25, 1),
            #    self.wnd.keys.D: (0.80, 1),
            #    self.wnd.keys.W: (1, 1.25),
            #    self.wnd.keys.S: (1, 0.80),
            #}
            #if key in zooms:
            #    zoom(view, *zooms[key], media.width()/2, media.height()/2)
            #    return
            #if key == self.wnd.keys.X:
            #    zoom(view, 1, view.w / view.h, media.width()/2, media.height()/2)
            #    return
            #if key == self.wnd.keys.Q:
            #    if plot.y_max > 0:
            #        view.y = 0.0
            #        view.h = 17/16 * plot.y_max
            #    else:
            #        view.y = 17/16 * plot.y_max
            #        view.h = 17/16 * abs(plot.y_max)
            #    media.view_set(*view.tuple())
            #    plot.is_reset = False
            #    return
            #if key == relf.wnd.keys.C:
            #    if plot.x_max > 0:
            #        view.x = 0.0
            #        view.w = 17/16 * abs(plot.x_max)
            #    else:
            #        view.x = 17/16 * plot.x_max
            #        view.w = 17/16 * abs(plot.x_max)
            #    media.view_set(*view.tuple())
            #    plot.is_reset = False
            #    return
            #if self.wnd.keys.Z:
            #    view.x = -17/16 * abs(plot.x_max)
            #    view.w = +34/16 * abs(plot.x_max)
            #    view.y = -17/16 * abs(plot.y_max)
            #    view.h = +34/16 * abs(plot.y_max)
            #    media.view_set(*view.tuple())
            #    plot.is_reset = False
            #    return
            #if self.wnd.keys.SPACE:
            #    reset()
            #    return

        def render(self, time, frametime):
            self.ctx.clear()
            for mode, first, count in plot.draws:
                self.va.render(mode=getattr(mgl, mode), first=first, vertices=count)
            #margin_x = 2.0 / media.width()  * view.w
            #margin_y = 2.0 / media.height() * view.h
            #aspect = media.height() / media.width() * view.w / view.h
            #text_h = 10.0/media.height()*view.h
            ## draw texts
            #for (s, x, y, r, g, b, a) in plot.texts:
            #    r, g, b, a = icolor(r, g, b, a)
            #    media.vector_text(s, x=x, y=y-text_h/4, h=text_h, aspect=aspect, r=r, g=g, b=b, a=a)
            #    media.line(x=x, y=y, w=text_h, h=0, r=r, g=g, b=b, a=a)
            #if not plot.hide_axes:
            #    # draw x axis
            #    increment = 10 ** int(math.log10(view.w))
            #    if view.w / increment < 2:
            #        increment /= 5
            #    elif view.w / increment < 5:
            #        increment /= 2
            #    i = view.x // increment * increment + increment
            #    while i < view.x + view.w:
            #        s = '{:.5}'.format(i)
            #        if view.x + view.w - i > increment:
            #            media.vector_text(s, x=i+margin_x, y=view.y+view.h-margin_y, h=text_h, aspect=aspect)
            #        media.line(xi=i, xf=i, y=view.y+view.h, h=-12.0/media.height()*view.h)
            #        i += increment
            #    # draw y axis
            #    increment = 10 ** int(math.log10(view.h))
            #    if view.h / increment < 2:
            #        increment /= 5
            #    elif view.h / increment < 5:
            #        increment /= 2
            #    i = (view.y + text_h + 2*margin_y) // increment * increment + increment
            #    while i < view.y + view.h - (text_h + 2*margin_y):
            #        s = '{:.5}'.format(-i)
            #        media.vector_text(s, x=view.x+margin_x, y=i-margin_y, h=text_h, aspect=aspect)
            #        media.line(x=view.x, w=12.0/media.width()*view.w, yi=i, yf=i)
            #        i += increment

    mglw.run_window_config(Config, args=(i for i in []))
