from . import media

import struct

vert_shader_src = b'''\
attribute vec2 aPosition;

varying vec2 vPosition;

void main() {
    gl_Position = vec4(
        aPosition.x,
        aPosition.y,
        0.0,
        1.0
    );
    vPosition = vec2(
        (aPosition.x + 1.0) / 2.0,
        (aPosition.y + 1.0) / 2.0
    );
}
'''

frag_shader_src = b'''\
#version 330

uniform sampler3D tData;

varying vec2 vPosition;

void main() {
    gl_FragColor = texture(tData, vec3(vPosition.xy, 0.5));
}
'''

class Plot:
    def __init__(
        self,
        title='plot',
        *,
        x_i, y_i, z_i,
        x_f, y_f, z_f,
        x_size, y_size, z_size,
    ):
        self.title = title
        self.x_i = x_i
        self.y_i = y_i
        self.z_i = z_i
        self.x_range = x_f - x_i
        self.y_range = y_f - y_i
        self.z_range = z_f - z_i
        self.x_size = x_size
        self.y_size = y_size
        self.z_size = z_size
        self.voxels = [0] * (x_size * y_size * z_size * 4)

    def voxel(self, x, y, z, r, g, b, a):
        i = int((x - self.x_i) / self.x_range * self.x_size)
        j = int((y - self.y_i) / self.y_range * self.y_size)
        k = int((z - self.z_i) / self.z_range * self.z_size)
        u = (
            + i * 4
            + j * self.z_size * 4
            + k * self.y_size * self.z_size * 4
        )
        self.voxels[u:u+4] = [r, g, b, a]

    def show(self, w=640, h=480):
        class U:
            t_data = media.gl.GLuint()
        media.init(
            w,
            h,
            self.title,
            program=(
                vert_shader_src,
                frag_shader_src,
                [],
                ['aPosition'],
            ),
        )
        buffer = media.Buffer()
        buffer.data = [
            -1, -1,
            +1, +1,
            -1, +1,
            -1, -1,
            +1, +1,
            +1, -1,
        ]
        # construct
        buffer.prep('static')
        buffer.draws = [('triangles', 0, len(buffer.data) // 2)]
        media.gl.glEnable(media.gl.GL_TEXTURE_3D)
        media.gl.glGenTextures(1, U.t_data)
        media.gl.glActiveTexture(media.gl.GL_TEXTURE0);
        media.gl.glBindTexture(media.gl.GL_TEXTURE_3D, U.t_data)
        media.gl.glTexParameteri(media.gl.GL_TEXTURE_3D, media.gl.GL_TEXTURE_MAG_FILTER, media.gl.GL_LINEAR);
        media.gl.glTexParameteri(media.gl.GL_TEXTURE_3D, media.gl.GL_TEXTURE_MIN_FILTER, media.gl.GL_LINEAR);
        media.gl.glTexParameteri(media.gl.GL_TEXTURE_3D, media.gl.GL_TEXTURE_WRAP_S, media.gl.GL_CLAMP_TO_EDGE);
        media.gl.glTexParameteri(media.gl.GL_TEXTURE_3D, media.gl.GL_TEXTURE_WRAP_T, media.gl.GL_CLAMP_TO_EDGE);
        media.gl.glTexParameteri(media.gl.GL_TEXTURE_3D, media.gl.GL_TEXTURE_WRAP_R, media.gl.GL_CLAMP_TO_EDGE);
        media.gl.glTexImage3D(
            media.gl.GL_TEXTURE_3D,
            0,
            media.gl.GL_RGBA,
            self.x_size,
            self.y_size,
            self.z_size,
            0,
            media.gl.GL_RGBA,
            media.gl.GL_FLOAT,
            bytes().join(struct.pack('f', i) for i in self.voxels),
        )
        # callbacks
        def draw():
            media.clear()
            buffer.draw(attributes=[('aPosition', 2)])
        media.set_callbacks(
            draw=draw,
        )
        # run
        media.run()
