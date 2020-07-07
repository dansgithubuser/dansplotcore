class Default:
    def __call__(self, x, y, i, series):
        colors = [
            (255, 255, 255),
            (255,   0,   0),
            (  0, 255,   0),
            (  0,   0, 255),
            (255, 255,   0),
            (  0, 255, 255),
            (255,   0, 255),
        ]
        color = colors[series % len(colors)]
        return {
            'x': x, 'y': y,
            'r': color[0], 'g': color[1], 'b': color[2],
        }

class Grid:
    def __init__(self, cell_w, cell_h, grid_w):
        self.cell_w = cell_w
        self.cell_h = cell_h
        self.grid_w = grid_w

    def __call__(self, x, y, i, series):
        dx = self.cell_w * (series % self.grid_w)
        dy = -self.cell_h * (series // self.grid_w)
        return {'x': x + dx, 'y': y + dy}
