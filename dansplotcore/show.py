from . import media

import copy
import math
import os
import re
import sys

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

def construct(plot, view, w, h):
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
    points = media.Vao()
    for x, y, r, g, b, a in plot.points:
        points.add(x, y, *fcolor(r, g, b, a))
    # lines
    lines = media.Vao('lines')
    for xi, yi, xf, yf, r, g, b, a in plot.lines:
        lines.add(xi, yi, *fcolor(r, g, b, a))
        lines.add(xf, yf, *fcolor(r, g, b, a))
    # rects
    rects = media.Vao('triangles')
    for xi, yi, xf, yf, r, g, b, a in plot.rects:
        rects.add(xi, yi, *fcolor(r, g, b, a))
        rects.add(xf, yf, *fcolor(r, g, b, a))
        rects.add(xi, yf, *fcolor(r, g, b, a))
        rects.add(xi, yi, *fcolor(r, g, b, a))
        rects.add(xf, yf, *fcolor(r, g, b, a))
        rects.add(xf, yi, *fcolor(r, g, b, a))
    # order
    plot.vaos = [rects, lines, points]

def show(plot, w, h):
    media.init(w, h, title=plot.title)
    dragging = False
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

    reset()
    construct(plot, view, w, h)

    class Callbacks:
        def resize(w, h):
            zoom(view, w/media.width(), h/media.height(), w/2, h/2)
            if plot.late_vertexors:
                construct(plot, view, media.width(), media.height())

        def left_mouse_button(pressed, x, y):
            dragging = pressed
            if dragging:
                drag_prev = (x, y)

        def mouse_move(x, y):
            mouse = x, y
            if dragging:
                xi, yi = drag_prev
                dx, dy = mouse[0]-xi, mouse[1]-yi
                move(view, dx, dy)
                drag_prev = mouse

        def mouse_wheel(delta):
            z = 1.25 if delta > 0 else 0.8
            zoom(view, z, z, mouse[0], mouse[1])

        def key_pressed(key):
            moves = {
                'Left' : ( 10,   0),
                'Right': (-10,   0),
                'Up'   : (  0,  10),
                'Down' : (  0, -10),
            }
            if key in moves:
                move(view, *moves[key])
                return
            zooms = {
                'a': (1.25, 1),
                'd': (0.80, 1),
                'w': (1, 1.25),
                's': (1, 0.80),
            }
            if key in zooms:
                zoom(view, *zooms[key], media.width()/2, media.height()/2)
                return
            if key == 'x':
                zoom(view, 1, view.w / view.h, media.width()/2, media.height()/2)
                return
            if key == 'q':
                if plot.y_max > 0:
                    view.y = 0.0
                    view.h = 17/16 * plot.y_max
                else:
                    view.y = 17/16 * plot.y_max
                    view.h = 17/16 * abs(plot.y_max)
                media.view_set(*view.tuple())
                plot.is_reset = False
                return
            if key == 'c':
                if plot.x_max > 0:
                    view.x = 0.0
                    view.w = 17/16 * abs(plot.x_max)
                else:
                    view.x = 17/16 * plot.x_max
                    view.w = 17/16 * abs(plot.x_max)
                media.view_set(*view.tuple())
                plot.is_reset = False
                return
            if key == 'z':
                view.x = -17/16 * abs(plot.x_max)
                view.w = +34/16 * abs(plot.x_max)
                view.y = -17/16 * abs(plot.y_max)
                view.h = +34/16 * abs(plot.y_max)
                media.view_set(*view.tuple())
                plot.is_reset = False
                return
            if key == 'Space':
                reset()
                return
            if key == 'Return':
                media.capture_start()
                return

        def draw():
            media.clear()
            for i in plot.vaos: i.draw()
            margin_x = 2.0 / media.width()  * view.w
            margin_y = 2.0 / media.height() * view.h
            aspect = media.height() / media.width() * view.w / view.h
            text_h = 10.0/media.height()*view.h
            # draw texts
            for (s, x, y, r, g, b, a) in plot.texts:
                r, g, b, a = fcolor(r, g, b, a)
                media.vector_text(s, x=x, y=y-text_h/4, h=text_h, aspect=aspect, r=r, g=g, b=b, a=a)
                media.line(x=x, y=y, w=text_h, h=0, r=r, g=g, b=b, a=a)
            if not plot.hide_axes:
                # draw x axis
                increment = 10 ** int(math.log10(view.w))
                if view.w / increment < 2:
                    increment /= 5
                elif view.w / increment < 5:
                    increment /= 2
                i = view.x // increment * increment + increment
                while i < view.x + view.w:
                    s = '{:.5}'.format(i)
                    if view.x + view.w - i > increment:
                        media.vector_text(s, x=i+margin_x, y=view.y+view.h-margin_y, h=text_h, aspect=aspect)
                    media.line(xi=i, xf=i, y=view.y+view.h, h=-12.0/media.height()*view.h)
                    i += increment
                # draw y axis
                increment = 10 ** int(math.log10(view.h))
                if view.h / increment < 2:
                    increment /= 5
                elif view.h / increment < 5:
                    increment /= 2
                i = (view.y + text_h + 2*margin_y) // increment * increment + increment
                while i < view.y + view.h - (text_h + 2*margin_y):
                    s = '{:.5}'.format(-i)
                    media.vector_text(s, x=view.x+margin_x, y=i-margin_y, h=text_h, aspect=aspect)
                    media.line(x=view.x, w=12.0/media.width()*view.w, yi=i, yf=i)
                    i += increment
            # display
            media.capture_finish(plot.title+'.png')

    media.loop(Callbacks)
