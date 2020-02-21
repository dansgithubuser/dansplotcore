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
