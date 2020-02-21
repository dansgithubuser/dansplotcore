import dansplotcore

import random

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

print('plotting random dots and lines, in (x=512..767, y=768..1023), reddish on right, greenish on top')
plot = dansplotcore.Plot('test')

for i in range(10000):
	x, y = random_position()
	r, g, b, a = random_color_for_position(x, y)
	if random.randint(0, 1):
		xf, yf = random_position()
		plot.line(x, y, xf, yf, r, g, b, a//4)
	else:
		plot.point(x, y, r, g, b, a)

plot.show()
