glyphs = {
    # numpad
    'N7I': [0, 2],
    'N8I': [1, 2],
    'N9I': [2, 2],
    'N4I': [0, 1],
    'N5I': [1, 1],
    'N6I': [2, 1],
    'N1I': [0, 0],
    'N2I': [1, 0],
    'N3I': [2, 0],

    'N7': ['N7I', 'N7I'],
    'N8': ['N8I', 'N8I'],
    'N9': ['N9I', 'N9I'],
    'N4': ['N4I', 'N4I'],
    'N5': ['N5I', 'N5I'],
    'N6': ['N6I', 'N6I'],
    'N1': ['N1I', 'N1I'],
    'N2': ['N2I', 'N2I'],
    'N3': ['N3I', 'N3I'],

    # under
    'U1I': [0, -1],
    'U2I': [1, -1],
    'U3I': [2, -1],

    'U1': ['U1I', 'U1I'],
    'U2': ['U2I', 'U2I'],
    'U3': ['U3I', 'U3I'],

    # lowercase mid
    'L1I': [0, 0.5],
    'L2I': [1, 0.5],
    'L3I': [2, 0.5],

    'L1': ['L1I', 'L1I'],
    'L2': ['L2I', 'L2I'],
    'L3': ['L3I', 'L3I'],

    # horizontal lines
    'L79': ['N7I', 'N9I'],
    'L46': ['N4I', 'N6I'],
    'L13': ['N1I', 'N3I'],

    # vertical lines
    'L71': ['N7I', 'N1I'],
    'L82': ['N8I', 'N2I'],
    'L93': ['N9I', 'N3I'],

    # 25-point grid
    'T15I': [0.0, 2.0],
    'T25I': [0.5, 2.0],
    'T35I': [1.0, 2.0],
    'T45I': [1.5, 2.0],
    'T55I': [2.0, 2.0],

    'T14I': [0.0, 1.5],
    'T24I': [0.5, 1.5],
    'T34I': [1.0, 1.5],
    'T44I': [1.5, 1.5],
    'T54I': [2.0, 1.5],

    'T13I': [0.0, 1.0],
    'T23I': [0.5, 1.0],
    'T33I': [1.0, 1.0],
    'T43I': [1.5, 1.0],
    'T53I': [2.0, 1.0],

    'T12I': [0.0, 0.5],
    'T22I': [0.5, 0.5],
    'T32I': [1.0, 0.5],
    'T42I': [1.5, 0.5],
    'T52I': [2.0, 0.5],

    'T11I': [0.0, 0.0],
    'T21I': [0.5, 0.0],
    'T31I': [1.0, 0.0],
    'T41I': [1.5, 0.0],
    'T51I': [2.0, 0.0],

    'T15': ['T15I', 'T15I'],
    'T25': ['T25I', 'T25I'],
    'T35': ['T35I', 'T35I'],
    'T45': ['T45I', 'T45I'],
    'T55': ['T55I', 'T55I'],

    'T14': ['T14I', 'T14I'],
    'T24': ['T24I', 'T24I'],
    'T34': ['T34I', 'T34I'],
    'T44': ['T44I', 'T44I'],
    'T54': ['T54I', 'T54I'],

    'T13': ['T13I', 'T13I'],
    'T23': ['T23I', 'T23I'],
    'T33': ['T33I', 'T33I'],
    'T43': ['T43I', 'T43I'],
    'T53': ['T53I', 'T53I'],

    'T12': ['T12I', 'T12I'],
    'T22': ['T22I', 'T22I'],
    'T32': ['T32I', 'T32I'],
    'T42': ['T42I', 'T42I'],
    'T52': ['T52I', 'T52I'],

    'T11': ['T11I', 'T11I'],
    'T21': ['T21I', 'T21I'],
    'T31': ['T31I', 'T31I'],
    'T41': ['T41I', 'T41I'],
    'T51': ['T51I', 'T51I'],

    # subglyphs
    'DOT': [1, 0.1, 1, -0.1],

    # characters
    ' ' : [],
    '\n': [],
    '!' : ['N8I', 'L2I', 'DOT'],
    '"' : ['T25I', 'T24I', 'T45I', 'T44I'],
    '#' : ['T25I', 'T21I', 'T45I', 'T41I', 'T14I', 'T54I', 'T12I', 'T52I'],
    '$' : ['T54I', 'T14', 'N4', 'N6', 'T52', 'T12I', 'L82'],
    '%' : ['N1I', 'N9I',  0, 2, 0, 1.8,  2, 0, 2, 0.2],
    '&' : ['N3I', 'T14', 'T25', 'T34', 'T12', 'T21', 'N2', 'N6I'],
    '\'': ['N8I', 'T34I'],
    '(' : ['T45I', 'T24', 'T22', 'T41I'],
    ')' : ['T25I', 'T44', 'T42', 'T21I'],
    '*' : ['N8I', 'N5I',  0.5, 1.7, 1.5, 1.3,  0.5, 1.3, 1.5, 1.7],
    '+' : ['L1I', 'L3I', 'N5I', 'N2I'],
    ',' : ['N2I',  0.8, -0.5],
    '-' : ['L1I', 'L3I'],
    '.' : ['DOT'],
    '/' : ['N1I', 'N9I'],
    '0' : ['O', 'N1I', 'N9I'],
    '1' : ['N7I', 'N8', 'N2I', 'N1I', 'N3I'],
    '2' : ['N7I', 'N9', 'N6', 'N4', 'N1', 'N3I'],
    '3' : ['N7I', 'N9', 'N6', 'N4I', 'N6I', 'N3', 'N1I'],
    '4' : ['N6I', 'N4', 'N9', 'N3I'],
    '5' : ['N9I', 'N7', 'N4', 'N6', 'N3', 'N1I'],
    '6' : ['N9I', 'N7', 'N1', 'N3', 'N6', 'N4I'],
    '7' : ['N7I', 'N9', 'N3I'],
    '8' : ['O', 'L46'],
    '9' : ['N6I', 'N4', 'N7', 'N9', 'N3', 'N1I'],
    ':' : ['DOT',  1, 1.1, 1, 0.9],
    ';' : ['N2I',  0.8, -0.5,  1, 1.1, 1, 0.9],
    '<' : ['N6I', 'L1', 'N3I'],
    '=' : ['L46', 'L1I', 'L3I'],
    '>' : ['N4I', 'L3', 'N1I'],
    '?' : ['N7I', 'N9', 'N6', 'N5', 'T32I', 'DOT'],
    '@' : ['N6I', 'N5', 'N2', 'N3', 'N9', 'N7', 'N1I'],
    'A' : ['L71', 'L79', 'L93', 'L46'],
    'B' : ['N7I', 'N1', 'N3', 'N6', 'N4I', 'N7I', 'N8', 'N5I'],
    'C' : ['L79', 'L71', 'L13'],
    'D' : ['N7I', 'N1', 'N2', 'N6', 'N8', 'N7I'],
    'E' : ['L71', 'L13', 'L46', 'L79'],
    'F' : ['L71', 'L46', 'L79'],
    'G' : ['N5I', 'N6', 'N3', 'N1', 'N7', 'N9I'],
    'H' : ['L71', 'L93', 'L46'],
    'I' : ['L82', 'L79', 'L13'],
    'J' : ['N8I', 'N2', 'N1I', 'L79'],
    'K' : ['L71', 'N9I', 'N4', 'N3I'],
    'L' : ['L71', 'L13'],
    'M' : ['N1I', 'N7', 'N5', 'N9', 'N3I'],
    'N' : ['N1I', 'N7', 'N3', 'N9I'],
    'O' : ['N7I', 'N9', 'N3', 'N1', 'N7I'],
    'P' : ['N1I', 'N7', 'N9', 'N6', 'N4I'],
    'Q' : ['O', 'N5I', 'N3I'],
    'R' : ['N1I', 'N7', 'N9', 'N6', 'N4', 'N3I'],
    'S' : ['N9I', 'N7', 'N4', 'N6', 'N3', 'N1I'],
    'T' : ['L82', 'L79'],
    'U' : ['N7I', 'N1', 'N3', 'N9I'],
    'V' : ['N7I', 'N2', 'N9I'],
    'W' : ['N7I', 'N1', 'N5', 'N3', 'N9I'],
    'X' : ['N7I', 'N3I', 'N1I', 'N9I'],
    'Y' : ['N9I', 'N1I', 'N7I', 'N5I'],
    'Z' : ['N7I', 'N9', 'N1', 'N3I'],
    '[' : ['T45I', 'T25', 'T21', 'T41I'],
    '\\': ['N7I', 'N3I'],
    ']' : ['T25I', 'T45', 'T41', 'T21I'],
    '^' : ['T24I', 'N8', 'T44I'],
    '_' : ['L13'],
    '`' : ['T25I', 'T43I'],
    'a' : ['N4I', 'N6', 'N3', 'N1', 'L1', 'L3I'],
    'b' : ['N7I', 'N1', 'N3', 'N6', 'N4I'],
    'c' : ['N6I', 'N4', 'N1', 'N3I'],
    'd' : ['N6I', 'N4', 'N1', 'N3', 'N9I'],
    'e' : ['L1I', 'L3', 'N6', 'N4', 'N1', 'N3I'],
    'f' : ['N2I', 'N8', 'N9I', 'L46'],
    'g' : ['N3I', 'N1', 'N4', 'N6', 'U3', 'U1I'],
    'h' : ['L71', 'N4I', 'N6', 'N3I'],
    'i' : ['N5I', 'N2I', 1, 1.4, 1, 1.6],
    'j' : ['N5I', 'U2', 'U1I', 1, 1.4, 1, 1.6],
    'k' : ['N7I', 'N1I', 'N6I', 'L1', 'N3I'],
    'l' : ['L82'],
    'm' : ['N1I', 'N4', 'N5', 'N2I', 'N5I', 'N6', 'N3I'],
    'n' : ['N1I', 'N4', 'N6', 'N3I'],
    'o' : ['N4I', 'N6', 'N3', 'N1', 'N4I'],
    'p' : ['U1I', 'N4', 'N6', 'N3', 'N1I'],
    'q' : ['U3I', 'N6', 'N4', 'N1', 'N3I'],
    'r' : ['N4I', 'N1I', 'L1I', 'N6I'],
    's' : ['N6I', 'N4', 'L1', 'L3', 'N3', 'N1I'],
    't' : ['L82', 'L46'],
    'u' : ['N4I', 'N1', 'N3', 'N6I'],
    'v' : ['N4I', 'N2', 'N6I'],
    'w' : ['N4I', 'N1', 'L2', 'N3', 'N6I'],
    'x' : ['N4I', 'N3I', 'N1I', 'N6I'],
    'y' : ['N6I', 'U1I', 'N4I', 'N2I'],
    'z' : ['N4I', 'N6', 'N1', 'N3I'],
    '{' : ['T45I', 'N8', 'T34', 'T23', 'T32', 'N2', 'T41I'],
    '|' : ['L82'],
    '}' : ['T25I', 'N8', 'T34', 'T43', 'T32', 'N2', 'T21I'],
    '~' : ['T13I', 'T24', 'T33', 'T42', 'T53I'],

    # glyph for unhandled character
    None: ['O', 'N7I', 'N3I', 'N1I', 'N9I'],
}

class Texter:
    def __init__(self):
        self.data = [];
        self.bounds = None

    def text(self, s, x, y, w, h, r=1.0, g=1.0, b=1.0, a=1.0):
        if not self.bounds:
            self.bounds = [x, y, x, y]
        x_i = x
        for c in s:
            self.glyph(c, x, y, w, h, r, g, b, a)
            x += w
            self.bounds[0] = min(self.bounds[0], x)
            self.bounds[2] = max(self.bounds[2], x)
            if c == '\n':
                x = x_i
                y -= h * 2
            self.bounds[1] = min(self.bounds[1], y)
            self.bounds[3] = max(self.bounds[3], y)

    def glyph(self, c, x, y, w, h, r, g, b, a):
        glyph = glyphs.get(c, glyphs[None])
        i = 0
        while i < len(glyph):
            if type(glyph[i]) == str:
                self.glyph(glyph[i], x, y, w, h, r, g, b, a)
                i += 1
            else:
                self.data.extend([
                    x + glyph[i + 0] / 3 * w,
                    y + glyph[i + 1] / 2 * h,
                    r, g, b, a,
                ])
                i += 2
