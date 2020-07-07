def default(x, y, i, series):
    colors = [
        (255, 255, 255),
        (255,   0,   0),
        (  0, 255,   0),
        (  0,   0, 255),
        (255, 255,   0),
        (  0, 255, 255),
        (255,   0, 255),
    ]
    color = colors[series%len(colors)]
    return {
        'x': x, 'y': y,
        'r': color[0], 'g': color[1], 'b': color[2],
        'a': 255,
    }
