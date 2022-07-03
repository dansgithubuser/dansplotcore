#===== imports =====#
import numpy as np
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt

#===== consts =====#
vert_shader = '''\
#version 330

uniform vec2 u_pos;
uniform vec2 u_zoom;

in vec2 a_pos;
in vec4 a_color;

out vec4 v_color;

void main() {
    gl_Position = vec4(
        (a_pos.x - u_pos.x) / u_zoom.x,
        (a_pos.y - u_pos.y) / u_zoom.y,
        0.0,
        1.0
    );
    v_color = a_color;
}
'''

frag_shader = '''\
#version 330

in vec4 v_color;

out vec4 o_color;

void main() {
    o_color = v_color;
}
'''

#===== file-scope vars =====#
class F:
    app = QtWidgets.QApplication([])
    window = None

#===== helpers =====#
def create_vbo(gl, data, size_per_vert, program, attrib_name):
    vbo = QtGui.QOpenGLBuffer(QtGui.QOpenGLBuffer.VertexBuffer)
    vbo.create()
    vbo.bind()
    data = np.array(data, np.float32)
    vbo.allocate(data, data.shape[0] * data.itemsize)
    attrib_index = program.attributeLocation(attrib_name)
    program.enableAttributeArray(attrib_index)
    program.setAttributeBuffer(attrib_index, gl.GL_FLOAT, 0, size_per_vert)
    vbo.release()
    return vbo

class Window(QtGui.QOpenGLWindow):
    def __init__(self):
        super().__init__()
        self.pos = [0.0, 0.0]
        self.zoom = [1.0, 1.0]

    #===== qt methods =====#
    def initializeGL(self):
        self.profile = QtGui.QOpenGLVersionProfile()
        for i in range(20, 100):
            self.profile.setVersion(i // 10, i % 10)
            try:
                gl = self.context().versionFunctions(self.profile)
            except ModuleNotFoundError:
                continue
            if gl: break
        self.gl = gl
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_DST_ALPHA)
        # program
        self.program = QtGui.QOpenGLShaderProgram(self)
        self.program.addShaderFromSourceCode(QtGui.QOpenGLShader.Vertex, vert_shader)
        self.program.addShaderFromSourceCode(QtGui.QOpenGLShader.Fragment, frag_shader)
        self.program.link()
        # uniforms
        self.set_u_pos()
        self.set_u_zoom()

    def paintGL(self):
        self.program.bind()
        F.callbacks.draw()
        self.program.release()

    def resizeEvent(self, event):
        size = event.size()
        F.callbacks.resize(size.width(), size.height())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            F.callbacks.left_mouse_button(True, pos.x(), pos.y())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.pos()
            F.callbacks.left_mouse_button(False, pos.x(), pos.y())

    def mouseMoveEvent(self, event):
        pos = event.pos()
        F.callbacks.mouse_move(pos.x(), pos.y())

    def wheelEvent(self, event):
        F.callbacks.mouse_wheel(event.angleDelta().y())

    def keyPressEvent(self, event):
        key = {
            Qt.Key_Left: 'Left',
            Qt.Key_Right: 'Right',
            Qt.Key_Up: 'Up',
            Qt.Key_Down: 'Down',
            Qt.Key_Space: 'Space',
            Qt.Key_Return: 'Return',
        }.get(event.key())
        if not key:
            key = chr(event.key()).lower()
        F.callbacks.key_pressed(key)

    #===== helpers =====#
    def set_u_pos(self):
        self.program.bind()
        self.program.setUniformValue('u_pos', *self.pos)
        self.program.release()

    def set_u_zoom(self):
        self.program.bind()
        self.program.setUniformValue('u_zoom', *self.zoom)
        self.program.release()

def xi_yi_from_kwargs(**kwargs):
    if 'bounds' in kwargs:
        xi, yi, xf, yf = kwargs['bounds']
    if 'xi' in kwargs:
        xi = kwargs['xi']
        xf = kwargs['xf']
    if 'yi' in kwargs:
        yi = kwargs['yi']
        yf = kwargs['yf']
    if 'x' in kwargs:
        xi = kwargs['x']
        xf = xi+kwargs['w']
    if 'y' in kwargs:
        yi = kwargs['y']
        yf = yi+kwargs['h']
    if kwargs.get('right', False):
        d = xf-xi
        xi -= d
        xf -= d
    if kwargs.get('bottom', False):
        d = yf-yi
        yi -= d
        yf -= d
    if kwargs.get('middle_x', False):
        d = (xf-xi)/2
        xi -= d
        xf -= d
    if kwargs.get('middle_y', False):
        d = (yf-yi)/2
        yi -= d
        yf -= d
    return (xi, yi, xf, yf)

def color_from_kwargs(**kwargs):
    r = kwargs.get('r', 1.0)
    g = kwargs.get('g', 1.0)
    b = kwargs.get('b', 1.0)
    a = kwargs.get('a', 1.0)
    c = kwargs.get('color', ())
    if   len(c) == 3: r, g, b    = c
    elif len(c) == 4: r, g, b, a = c
    return (r, g, b, a)

# ===== interface =====#
def init(w, h, title):
    F.window = Window()
    F.window.resize(w, h)
    F.window.setTitle(title)
    F.window.show()

def width():
    return F.window.width()

def height():
    return F.window.height()

def view_set(x, y, w, h):
    F.window.pos = (x, y)
    F.window.zoom = (w, h)
    if hasattr(F.window, 'program'):
        F.window.set_u_pos()
        F.window.set_u_zoom()
        F.window.update()

def clear():
    gl = F.window.gl
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

def capture_start():
    print('capture_start unimplemented')

def capture_finish(file_name):
    print('capture_finish unimplemented')

class Vao:
    def __init__(self, kind='points'):
        self.verts = []
        self.kind = kind
        self.vao = None

    def add(self, x, y, r, g, b, a):
        self.verts.append([x, y, r, g, b, a])

    def prep(self, gl, program, window):
        self.vao = QtGui.QOpenGLVertexArrayObject(window)
        self.vao.create()
        self.vao.bind()
        self.vbo_pos = create_vbo(
            gl,
            [j for i in self.verts for j in i[0:2]],
            2,
            program,
            'a_pos',
        )
        self.vbo_color = create_vbo(
            gl,
            [j for i in self.verts for j in i[2:6]],
            4,
            program,
            'a_color',
        )
        self.vao.release()

    def draw(self):
        gl = F.window.gl
        if not self.vao:
            self.prep(gl, F.window.program, F.window)
        self.vao.bind()
        gl.glDrawArrays(getattr(gl, f'GL_{self.kind.upper()}'), 0, len(self.verts))
        self.vao.release()

def vector_text(s, **kwargs):
    kwargs['xf'] = 0
    kwargs['w' ] = 0
    xi, yi, xf, yf = xi_yi_from_kwargs(**kwargs)
    r, g, b, a = color_from_kwargs(**kwargs)
    aspect = kwargs.get('aspect', 1)
    print('vector_text unimplemented')

def line(**kwargs):
    xi, yi, xf, yf = xi_yi_from_kwargs(**kwargs)
    r, g, b, a = color_from_kwargs(**kwargs)
    print('line unimplemented')

def loop(callbacks):
    F.callbacks = callbacks
    F.app.exec()
