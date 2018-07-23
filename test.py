import dansplotcore

import random

plot=dansplotcore.Plot('test')

for i in range(100):
	plot.point(*(random.randint(0, 255) for i in range(6)))

plot.show()
