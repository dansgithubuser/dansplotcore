import math
import os
import re
import sys
import time

LOC=os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(LOC, 'danssfml', 'wrapper'))

try:
	import media
except:
	from danssfmlpy import media

class Plot:
	def __init__(self, title):
		self.title=title
		self.points=[]
		self.x_min= math.inf
		self.x_max=-math.inf
		self.y_min= math.inf
		self.y_max=-math.inf

	def point(self, x, y, r, g, b, a):
		y=-y
		self.points.append([x, y, r, g, b, a])
		self.x_min=min(x, self.x_min)
		self.x_max=max(x, self.x_max)
		self.y_min=min(y, self.y_min)
		self.y_max=max(y, self.y_max)

	def show(self, w=640, h=480, pixels_per_unit=1):
		media.init(w, h, title=self.title)
		media.custom_resize(True)
		done=False
		dragging=False
		mouse=[0, 0]
		view=[self.x_min, self.y_min, self.x_max-self.x_min, self.y_max-self.y_min]
		screen=[media.width(), media.height()]
		media.view_set(*view)
		view=list(media.view_get())
		def move(view, dx, dy):
			view[0]-=dx*view[2]/media.width()
			view[1]-=dy*view[3]/media.height()
			media.view_set(*view)
		def zoom(view, zx, zy, x, y):
			#change view st (x, y) stays put and (w, h) multiplies by (zx, zy)
			new_view_w=view[2]*zx
			new_view_h=view[3]*zy
			view[0]+=1.0*x/media.width ()*(view[2]-new_view_w)
			view[1]+=1.0*y/media.height()*(view[3]-new_view_h)
			view[2]=new_view_w
			view[3]=new_view_h
			media.view_set(*view)
		self._construct(pixels_per_unit)
		while not done:
			#handle events
			while True:
				event=media.poll_event()
				if not event: break
				#quit
				if event=='q': done=True; break
				#resize
				m=re.match(r'rw(\d+)h(\d+)', event)
				if m:
					w, h=(int(i) for i in m.groups())
					zoom(view, 1.0*w/screen[0], 1.0*h/screen[1], w/2, h/2)
					screen=[w, h]
					break
				#left mouse button
				if event[0]=='b':
					dragging={'<': True, '>': False}[event[1]]
					if dragging:
						m=re.match(r'b<0x(\d+)y(\d+)', event)
						drag_prev=(int(i) for i in m.groups())
					break
				#mouse move
				m=re.match(r'x(\d+)y(\d+)', event)
				if m:
					mouse=[int(i) for i in m.groups()]
					if dragging:
						xi, yi=drag_prev
						dx, dy=mouse[0]-xi, mouse[1]-yi
						move(view, dx, dy)
						drag_prev=mouse
					break
				#mouse wheel
				if event.startswith('w'):
					delta=int(event[1:])
					z=1.25 if delta>0 else 0.8
					zoom(view, z, z, mouse[0], mouse[1])
				#keyboard
				m=re.match('<(.+)', event)
				if m:
					key=m.group(1)
					moves={
						'Left' : ( 10,   0),
						'Right': (-10,   0),
						'Up'   : (  0,  10),
						'Down' : (  0, -10),
					}
					if key in moves:
						move(view, *moves[key])
						break
					zooms={
						'a': (1.25, 1),
						'd': (0.80, 1),
						'w': (1, 1.25),
						's': (1, 0.80),
					}
					if key in zooms:
						zoom(view, *zooms[key], media.width()/2, media.height()/2)
						break
					if key=='Return': media.capture_start()
			#draw
			media.clear(color=(0, 0, 0))
			self.construction.draw(self.x_min, -255)
			margin_x=2.0/screen[0]*view[2]
			margin_y=2.0/screen[1]*view[3]
			##x axis
			i=view[0]+view[2]/8
			while i<view[0]+15*view[2]/16:
				s='{:.8}'.format(i)
				media.vector_text(s, x=i+margin_x, y=view[1]+view[3]-margin_y, h=8.0/screen[1]*view[3])
				media.line(xi=i, xf=i, y=view[1]+view[3], h=-12.0/screen[1]*view[2])
				i+=view[2]/8
			##y axis
			i=view[1]+view[3]/8
			while i<view[1]+15*view[3]/16:
				s='{:.8}'.format(-i)
				media.vector_text(s, x=view[0]+margin_x, y=i-margin_y, h=8.0/screen[1]*view[3])
				media.line(x=view[0], w=12.0/screen[0]*view[2], yi=i, yf=i)
				i+=view[2]/8
			##display
			media.display()
			media.capture_finish('plot.png')
			time.sleep(0.01)

	def _construct(self, pixels_per_unit):
		vertex_buffer=media.VertexBuffer(len(self.points))
		for i, point in enumerate(self.points):
			point[0]-=self.x_min
			point[1]-=self.y_min
			point[0]*=pixels_per_unit
			point[1]*=pixels_per_unit
			vertex_buffer.update(i, *point)
		view=media.view_get()
		self.construction=media.RenderTexture(
			int(pixels_per_unit*view[2]),
			int(pixels_per_unit*view[3]),
		)
		media.target_set(self.construction)
		vertex_buffer.draw()
		media.target_reset()
