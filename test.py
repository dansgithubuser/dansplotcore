#!/usr/bin/env python3

import dansplotcore as dpc

import argparse
import collections
import datetime
import math
import random
import string

parser = argparse.ArgumentParser()
parser.add_argument('case', default='all', nargs='?')
args = parser.parse_args()

def random_position():
    x = random.randint(512, 767)
    y = random.randint(768, 1023)
    return (x, y)

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    a = random.randint(0, 255)
    return (r, g, b, a)

def random_color_for_position(x, y):
    r = random.randint(0, 255) % (x-512+1)
    g = random.randint(0, 255) % (y-768+1)
    b = random.randint(0, 255)
    a = random.randint(0, 255)
    return (r, g, b, a)

#===== general =====#
if args.case in ['1', 'general', 'all']:
    print('''plotting random dots, lines, text, pluses:
        - in (x=512..767, y=768..1023)
        - reddish on right
        - greenish on top\
    ''')
    plot = dpc.Plot('test', x_axis_title='x-axis', y_axis_title='y-axis')

    for i in range(10000):
        x, y = random_position()
        r, g, b, a = random_color_for_position(x, y)
        choice = random.choice(['point', 'line', 'text', 'plus'])
        if choice == 'point':
            plot.point(x, y, r, g, b, a)
        elif choice == 'line':
            xf, yf = random_position()
            plot.line(x, y, xf, yf, r, g, b, a//4)
        elif choice == 'text' and not random.randint(0, 100):
            s = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(random.randint(1, 8)))
            plot.text(s, x, y, r, g, b, a)
        elif choice == 'plus' and not random.randint(0, 10):
            plot.late_vertexor(dpc.p.Plus().vertexor, x, y, r, g, b, a)

    plot.show()

#===== grid =====#
if args.case in ['2', 'grid', 'all']:
    print('''plotting a grid of simple plots:
        - lines with increasing slopes
        - sideways parabola; 3 parabolas getting wider
        - random dots; half-slope line\
    ''')
    size = 120
    plot = dpc.Plot(
        'test2',
        transform=dpc.transforms.Grid(size, size, 4),
        hide_axes=True,
    )

    plot.plot([i for i in range(size)])
    plot.plot([[i*j%size for i in range(size)] for j in range(2, 5)])

    plot.plot([(i-10)**2 for i in range(0, 20)], [i for i in range(0, 20)])
    plot.plot([[i*j%size for i in range(size)] for j in range(1, 4)], [i*i for i in range(10)])

    plot.plot({random.randint(0, size): random.randint(0, size) for i in range(size)})
    plot.plot(lambda x: x / 2, x=(0, size))

    plot.show()

#===== primitives =====#
if args.case in ['3', 'primitives', 'all']:
    print('''plotting:
        - a function with samples marked by pluses and connected by lines
        - a function with samples marked by crosses
    ''')
    plot = dpc.Plot()
    plot.set_primitive(
        dpc.primitives.Compound(
            dpc.primitives.Line(),
            dpc.primitives.Plus(),
        )
    )
    plot.plot(lambda x: x*x)
    plot.set_primitive(dpc.primitives.Cross())
    for i in range(-50, 50):
        x = i / 50
        y = i / 50
        plot.primitive(**plot.transform(x, y, i, plot.series))
    plot.show()

#===== compound transform =====#
if args.case in ['4', 'compound-transform', 'all']:
    print('''plotting white and red fences:
        - with increasing frequency
        - in upside-down-L-shaped groups of 3
        - in a grid with 3 columns
    ''')
    plot = dpc.Plot(
        'test4',
        transform=dpc.transforms.Compound(
            dpc.transforms.Grid(10, 8, 3),
            (dpc.transforms.Grid(3, 2, 2), 3),
            (dpc.transforms.Default(), 2),
        ),
        hide_axes=True,
    )
    for j in range(1, 31):
        for k in [-1, 1]:
            plot.plot(lambda i: k*j/10*i%1)
    plot.show()

#===== rects =====#
if args.case in ['5', 'rects', 'all']:
    print('''plotting rects
        - in a 5x5 grid
        - with random colors
    ''')
    plot = dpc.Plot('test5', hide_axes=True)
    for x in range(5):
        for y in range(5):
            color = random_color()
            plot.rect(x, y, x+1, y+1, *color)
            plot.text(f'{color}', x, y)
    plot.show()

#===== datetime =====#
if args.case in ['6', 'datetime', 'all']:
    print('''plotting linear datetime vs number
        - a point for the start of each month in 2000
        - y values are dates, axes show days since 2000 Jan 1
        - x values are numbers, days since 2000 Jan 1
        - "hello" in the top-left (dynamic)
        - "there" in the bottom-rigth (static)
    ''')
    dates = []
    for i in range(12):
        y = datetime.datetime(2000, i+1, 1)
        x = (y - datetime.datetime(2000, 1, 1)).total_seconds() / (24 * 60 * 60)
        dates.append((x, y))
    dates.reverse()
    plot = dpc.Plot(datetime_unit=24*60*60)
    plot.plot(dates)
    plot.text('hello', 0, datetime.datetime(2000, 12, 1))
    plot.text_static('there', 300, datetime.datetime(2000, 1, 1), w=5, h=10)
    plot.show()

#===== scatter plot with lines =====#
if args.case in ['7', 'scatter-line', 'all']:
    print('''plotting line scatterplot
        - x values are 0..6
        - y values are fibonacci
    ''')
    dpc.plot(
        [
            (0, 1),
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 5),
            (5, 8),
            (6, 13),
        ],
        transform=dpc.transforms.Default(colors=[dpc.transforms.Color(128, 128, 128)]),
        primitive=dpc.primitives.Line(),
    )

#===== text with max w and h =====#
if args.case in ['8', 'text-max-w-h', 'all']:
    print('''plotting texts:
        - As have max_w=1, max_h=1
        - Bs have max_w=1
        - Cs have max_h=1
        - D has scale=20
    ''')
    plot = dpc.Plot()
    plot.text('AA',  0, 10, max_w=1, max_h=1)
    plot.text('AA',  1, 10, max_w=1, max_h=1)
    plot.text('AA',  0, 11, max_w=1, max_h=1)
    plot.text('AA',  1, 11, max_w=1, max_h=1)
    plot.text('BB', 10, 10, max_w=1)
    plot.text('BB', 11, 10, max_w=1)
    plot.text('CC',  0,  0, max_h=1)
    plot.text('CC',  0,  1, max_h=1)
    plot.text('DD', 10,  0, scale=20)
    plot.show()

#===== 2d =====#
if args.case in ['9', '2d', 'all']:
    print('''plotting grid:
        - top left is bright
        - right is dimmer
        - bottom is dimmest
    ''')
    import numpy as np
    dpc.plot(np.array([
        [3, 2, 1, 0],
        [5, 4, 3, 2],
        [7, 6, 5, 4],
        [9, 8, 7, 6],
    ]))

#===== legend =====#
if args.case in ['10', 'legend', 'all']:
    print('plotting 3 functions with legend, colors')
    plot = dpc.Plot()
    plot.plot(lambda i: i, legend='x')
    plot.plot(lambda i: 2 * i, legend='2x')
    plot.plot(lambda i: math.sin(i), legend='sin(x)')
    plot.show()
    print('plotting 3 functions with legend, 2 per cell')
    plot = dpc.Plot(transform=dpc.t.Compound(dpc.t.Grid(2, 2, 2), (dpc.t.Default(), 2)))
    plot.plot(lambda i: i, legend='x')
    plot.plot(lambda i: 2 * i, legend='2x')
    plot.plot(lambda i: math.sin(i), legend='sin(x)')
    plot.show()

#===== histogram =====#
if args.case in ['11', 'histogram', 'all']:
    print('plotting histogram of a normal distribution')
    x = [random.gauss() for i in range(400)]
    dpc.plot(dpc.proc.bucket(x), primitive=dpc.p.Bar())

#===== empty =====#
if args.case in ['12', 'empty', 'all']:
    print('plotting empty plot')
    dpc.plot([])

#===== static text =====#
if args.case in ['13', 'static-text', 'all']:
    print('plotting a bunch of static text (rendering should be snappy)')
    plot = dpc.Plot()
    for i in range(300):
        plot.text_static(
            str(random.randint(0, 1e22)),
            (i % 5) * 30,
            (i // 5) * 1.5,
        )
    plot.show()

#===== heatmap =====#
if args.case in ['14', 'heatmap', 'all']:
    print('plotting heatmap')
    heatmap = collections.defaultdict(int)
    for i in range(1000):
        xy = (random.randint(0, 10), random.randint(0, 10))
        heatmap[xy] += random.randint(0, 10)
    plot = dpc.Plot()
    plot.plot_heatmap([(*xy, z) for xy, z in heatmap.items()])
    plot.show()

#===== log-log =====#
if args.case in ['15', 'log-log', 'all']:
    print('plotting 1, x, x ** 2, x ** 3 with log-log axes')
    plot = dpc.Plot(
        primitive=dpc.p.Line(),
        x_axis_transform=lambda x: 10 ** x,
        y_axis_transform=lambda y: 10 ** y,
    )
    for i in range(4):
        plot.plot([(math.log10(j), math.log10(j ** i)) for j in range(1, 101)])
    plot.show()

#===== contours =====#
if args.case in ['16', 'contours', 'all']:
    print('plotting contours of a y = quantized(randomized(x))')
    points = []
    for i in range(10000):
        x = i / 1000 + random.random()
        y = int(x * random.random())
        points.append((x, y))
    plot = dpc.Plot()
    dpc.process.contours(points, plot=plot)
    for point in points:
        plot.point(*point)
    plot.show()

#===== variables =====#
if args.case in ['17', 'variables', 'all']:
    print('making a plot with some variables (right-click drag to move)')
    plot = dpc.Plot()
    plot.plot(lambda x: x ** 2)
    a = plot.variable('a', 0, 1, 'x', home=(0, 0))
    b = plot.variable('b', 0, 0, 'y')
    c = plot.variable('c', 1, 1)
    plot.show()
    print('a =', a())
    print('b =', b())
    print('c =', c())

#===== voxel =====#
if args.case in ['18', 'voxel-basic', 'all', 'voxel']:
    import dansplotcore.voxel as voxel
    plot = voxel.Plot(
        x_i=-10, x_f=+10, x_size=20,
        y_i=-10, y_f=+10, y_size=20,
        z_i=-10, z_f=+10, z_size=20,
    )
    for i in range(-10, 10):
        for j in range(-10, 10):
            for k in range(-10, 10):
                x = i
                y = j
                z = k
                r = 1 / (1 + 2 ** (x * y))
                g = 1 / (1 + 2 ** (y * z))
                b = 1 / (1 + 2 ** (z * x))
                a = 2 ** (1 - (x ** 2 + y ** 2 + z ** 2)) / 2
                r = (x + 10) / 20
                g = (y + 10) / 20
                b = (z + 10) / 20
                a = 1.0
                plot.voxel(x, y, z, r, g, b, a)
    plot.show()

#===== 3d =====#
if args.case in ['19', 'volume', 'all', '3d']:
    import dansplotcore.threed as threed
    plot = threed.Plot()
    stride = 5
    zoom = 1
    for i in range(-100, 101, stride):
        for j in range(-100, 101, stride):
            for k in range(-100, 101, stride):
                x = i / zoom
                y = j / zoom
                z = k / zoom
                radius = (x ** 2 + y ** 2 + z ** 2) ** (1/2)
                theta = math.atan2(y, x)
                psi_100 = math.exp(-radius)
                psi_200 = (2 - radius) * math.exp(-radius / 2)
                psi_210 = radius * math.exp(-radius / 2) * math.cos(theta)
                psi_300 = (27 - 18 * radius + 2 * radius ** 2) * math.exp(-radius / 3)
                psi_310 = (6 * radius - radius ** 2) * math.exp(-radius / 3) * math.cos(theta)
                psi_320 = radius ** 2 * math.exp(-radius / 3) * (3 * math.cos(theta) ** 2 - 1)
                psi = psi_320
                r = 1.0 if psi > 0 else 0.0
                g = 0.0
                b = 1.0 if psi < 0 else 0.0
                a = abs(psi)
                plot.grid_cube(x, y, z, stride/zoom, r, g, b, a)
    plot.show()

#===== animation =====#
if args.case in ['20', 'animation', 'all']:
    print('animating a sliding sine wave')
    plot = dpc.Plot(primitive=dpc.p.Line())

    class Updater:
        def __init__(self):
            self.phase = 0

        def __call__(self, dt):
            plot.clear()
            self.phase += dt * math.tau
            plot.plot(lambda x: math.sin(x + self.phase), x=(0, 10))

    updater = Updater()
    updater(0)
    plot.show(update=updater)

#===== 3d animation =====#
if args.case in ['21', 'animation-3d', 'all']:
    print('animating a pulsing cube')
    import dansplotcore.threed as threed
    plot = threed.Plot()

    class Updater:
        def __init__(self):
            self.phase = 0

        def __call__(self, dt):
            plot.clear()
            self.phase += dt * math.tau
            n = 10
            for x in range(n):
                for y in range(n):
                    for z in range(n):
                        z -= n/2
                        d = max([abs(x - n/2), abs(y - n/2), abs(z), 1])
                        a = (math.sin(self.phase) + 1) / d
                        plot.grid_cube(x, y, z, 1, 1, 0, 0, a)

    updater = Updater()
    updater(0)
    plot.show(update=updater)
