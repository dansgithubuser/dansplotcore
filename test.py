import dansplotcore as dpc

import argparse
import random
import string

parser = argparse.ArgumentParser()
parser.add_argument('case', default='all', nargs='?')
args = parser.parse_args()

def random_position():
    x = random.randint(512, 767)
    y = random.randint(768, 1023)
    return (x, y)

def random_color_for_position(x, y):
    r = random.randint(0, 255) % (x-512+1)
    g = random.randint(0, 255) % (y-768+1)
    b = random.randint(0, 255)
    a = random.randint(0, 255)
    return (r, g, b, a)

#===== general =====#
if args.case in ['1', 'general', 'all']:
    print('plotting random dots, lines, text, in (x=512..767, y=768..1023), reddish on right, greenish on top')
    plot = dpc.Plot('test')

    for i in range(10000):
        x, y = random_position()
        r, g, b, a = random_color_for_position(x, y)
        choice = random.choice(['point', 'line', 'text'])
        if choice == 'point':
            plot.point(x, y, r, g, b, a)
        elif choice == 'line':
            xf, yf = random_position()
            plot.line(x, y, xf, yf, r, g, b, a//4)
        elif choice == 'text' and not random.randint(0, 100):
            s = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(random.randint(1, 8)))
            plot.text(s, x, y, r, g, b, a)

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
    plot.plot(lambda x: x)
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
