import dansplotcore as dpc

import argparse
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
    plot = dpc.Plot('test')

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
        elif choice == 'plus':
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
    print('''plotting linear relation vs datetime
        - x axis should show days since 2000 Jan 1
        - x values are beginning of each month in 2000
        - y values are days since 2000 Jan 1
    ''')
    dates = [datetime.datetime(2000, i+1, 1) for i in range(12)]
    dpc.plot([
        (
            (i - dates[0]).total_seconds() / (24 * 60 * 60),
            i,
        )
        for i in dates
    ])

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
    print('plotting 3 functions with legend, grid')
    plot = dpc.Plot(transform=dpc.t.Grid(2, 2, 2))
    plot.plot(lambda i: i, legend='x', legend_displacement=(0, 0))
    plot.plot(lambda i: 2 * i, legend='2x', legend_displacement=(0, 0))
    plot.plot(lambda i: math.sin(i), legend='sin(x)', legend_displacement=(0, 0))
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
