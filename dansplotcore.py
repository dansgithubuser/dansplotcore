import os
import sys
import time

LOC=os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(LOC, 'danssfml', 'wrapper'))

import media

class Plot:
	def __init__(self, title):
		self.title=title
		self.points=[]

	def point(self, x, y, r, g, b, a):
		self.points.append((x, y, r, g, b, a))

	def show(self):
		self._construct()
		media.init(title=self.title)
		done=False
		while not done:
			while True:
				event=media.poll_event()
				if not event: break
				if event=='q': done=True
			self.vertex_buffer.draw()
			media.display()
			time.sleep(0.01)

	def _construct(self):
		self.vertex_buffer=media.VertexBuffer(len(self.points))
		for i, point in enumerate(self.points):
			self.vertex_buffer.update(i, *point)
