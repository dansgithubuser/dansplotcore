import dansplotcore

import random
import string

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
print('plotting random dots, lines, text, in (x=512..767, y=768..1023), reddish on right, greenish on top')
plot = dansplotcore.Plot('test')

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
print('''plotting a grid of simple plots:
    - lines with increasing slopes
    - sideways parabola; 3 parabolas getting wider
    - random dots; half-slope line\
''')
size = 120
plot = dansplotcore.Plot(
    'test2',
    transform=dansplotcore.transforms.Grid(size, size, 4),
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
print('plotting a function with samples connected by lines')
dansplotcore.plot(lambda x: x*x, primitive=dansplotcore.primitives.Line())
