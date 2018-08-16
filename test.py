import dansplotcore

import random

plot=dansplotcore.Plot('test')

for i in range(10000):
	x=random.randint(0, 255)
	y=random.randint(0, 255)
	r=random.randint(0, 255)%(x+1)
	g=random.randint(0, 255)%(y+1)
	b=random.randint(0, 255)
	a=random.randint(0, 255)
	plot.point(x, y, r, g, b, a)

plot.show(pixels_per_unit=2)
