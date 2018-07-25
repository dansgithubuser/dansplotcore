import os
import re
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
		media.custom_resize(True)
		done=False
		dragging=False
		view=[0, 0, 0, 0]
		def move(view, dx, dy):
			view[0]-=dx; view[1]-=dy
			media.set_view(*view)
		while not done:
			while True:
				event=media.poll_event()
				if not event: break
				#quit
				if event=='q': done=True; break
				#resize
				m=re.match(r'rw(\d+)h(\d+)', event)
				if m:
					w, h=(int(i) for i in m.groups())
					view[2]=w; view[3]=h
					media.set_view(*view)
					break
				#left mouse button
				if event[0]=='b':
					dragging={'<': True, '>': False}[event[1]]
					if dragging:
						m=re.match(r'b<0x(\d+)y(\d+)', event)
						drag_prev=(int(i) for i in m.groups())
					break
				#mouse move
				if dragging:
					m=re.match(r'x(\d+)y(\d+)', event)
					(xf, yf)=(int(i) for i in m.groups())
					(xi, yi)=drag_prev
					(dx, dy)=(xf-xi, yf-yi)
					move(view, dx, dy)
					drag_prev=(xf, yf)
					break
				#keyboard
				m=re.match('<(.+)', event)
				if m:
					key=m.group(1)
					move(view, *{
						'Left' : ( 10,   0),
						'Right': (-10,   0),
						'Up'   : (  0,  10),
						'Down' : (  0, -10),
					}.get(key, (0, 0)))
			media.clear(color=(0, 0, 0))
			self.vertex_buffer.draw()
			media.display()
			time.sleep(0.01)

	def _construct(self):
		self.vertex_buffer=media.VertexBuffer(len(self.points))
		for i, point in enumerate(self.points):
			self.vertex_buffer.update(i, *point)
