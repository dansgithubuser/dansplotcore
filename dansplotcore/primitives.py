import weakref

class _Base:
    def set_plot(self, plot):
        self.plot = weakref.proxy(plot)
        return self

class Point(_Base):
    def __call__(self, x, y, r=255, g=255, b=255, a=255):
        self.plot.point(x, y, r, g, b, a)

class Line(_Base):
    def __init__(self):
        self.x = None
        self.y = None

    def __call__(self, x, y, r=255, g=255, b=255, a=255):
        if self.x:
            self.plot.line(self.x, self.y, x, y, r, g, b, a)
        else:
            self.plot.point(x, y, r, g, b, a)
        self.x = x
        self.y = y
