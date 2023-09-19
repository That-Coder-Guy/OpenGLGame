import math
import settings
from components import *
import OpenGL.GL as opengl
import OpenGL.GLU as openglu
import glfw as openglfw


class RenderTest(Scene):
    def __init__(self, window: Window):
        super().__init__(window=window)
        self.cube_vertices = ((0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 0),
                              (1, 0, 0), (1, 1, 1), (1, 1, 0), (1, 0, 1))
        self.cube_edges = ((0, 1), (0, 3), (0, 4), (1, 2), (1, 7), (2, 5),
                           (2, 3), (3, 6), (4, 6), (4, 7), (5, 6), (5, 7))
        self.cube_faces = ((0, 3, 6, 4), (2, 5, 6, 3), (7, 5, 2, 1),
                           (1, 0, 4, 7), (7, 4, 6, 5), (2, 3, 0, 1))
        self.position = [0.0, 0.0, 0.0]
        self.angle = [0.0, 0.0, 0.0]

    def setup(self) -> None:
        width, height = self.get_window().get_size()

        self.get_window().set_input_mode(openglfw.CURSOR, openglfw.CURSOR_DISABLED)
        self.get_window().set_cursor_position(width // 2, height // 2)

        # Enable back-face culling
        opengl.glEnable(opengl.GL_CULL_FACE)
        opengl.glCullFace(opengl.GL_BACK)

        # NOTE: Remember that enabling the depth buffer hides unneeded faces instead
        #       of not drawing that in the first place
        opengl.glEnable(opengl.GL_DEPTH_TEST)

    def update(self) -> None:
        width, height = self.get_window().get_size()

        cursor_position = self.get_window().get_cursor_position()
        cursor_velocity = (cursor_position[0] - (width // 2), cursor_position[1] - (height // 2))
        self.angle[0] = (self.angle[0] + cursor_velocity[0] / 8) % 360
        self.angle[1] = max(min(90.0, self.angle[1] + cursor_velocity[1] / 8), -90.0)
        self.get_window().set_cursor_position(width // 2, height // 2)

        if self.get_window().get_key(openglfw.KEY_W):
            self.position[0] -= math.sin((self.angle[0] / 180) * math.pi) * 0.1
            self.position[2] += math.cos((self.angle[0] / 180) * math.pi) * 0.1
        if self.get_window().get_key(openglfw.KEY_S):
            self.position[0] += math.sin((self.angle[0] / 180) * math.pi) * 0.1
            self.position[2] -= math.cos((self.angle[0] / 180) * math.pi) * 0.1
        if self.get_window().get_key(openglfw.KEY_A):
            self.position[0] += math.cos((self.angle[0] / 180) * math.pi) * 0.1
            self.position[2] += math.sin((self.angle[0] / 180) * math.pi) * 0.1
        if self.get_window().get_key(openglfw.KEY_D):
            self.position[0] -= math.cos((self.angle[0] / 180) * math.pi) * 0.1
            self.position[2] -= math.sin((self.angle[0] / 180) * math.pi) * 0.1

        if self.get_window().get_key(openglfw.KEY_SPACE):
            self.position[1] -= 0.1
        if self.get_window().get_key(openglfw.KEY_LEFT_SHIFT):
            self.position[1] += 0.1

        opengl.glLoadIdentity()
        opengl.glMatrixMode(opengl.GL_PROJECTION)
        openglu.gluPerspective(45, (width / max(1, height)), 0.1, 50.0)
        opengl.glRotatef(self.angle[1], True, False, False)
        opengl.glRotatef(self.angle[0], False, True, False)
        opengl.glTranslatef(*self.position)

    def draw_cube(self, x: float, y: float, z: float) -> None:
        opengl.glBegin(opengl.GL_QUADS)
        for face in self.cube_faces:
            for vertex in face:
                opengl.glVertex3fv((self.cube_vertices[vertex][0] + x,
                                    self.cube_vertices[vertex][1] + y,
                                    self.cube_vertices[vertex][2] + z))
        opengl.glEnd()

    def draw(self) -> None:
        opengl.glColor(1.0, 0.0, 0.0)
        self.draw_cube(0, 0, 0)
        opengl.glColor(0.0, 1.0, 0.0)
        self.draw_cube(1, 0, 0)
        opengl.glColor(0.0, 0.0, 1.0)
        self.draw_cube(0, 0, 1)
        opengl.glColor(1.0, 0.0, 0.0)
        self.draw_cube(1, 0, 1)
        opengl.glColor(0.0, 1.0, 0.0)
        self.draw_cube(2, 0, 2)


if __name__ == "__main__":
    game = Window()

    game.set_size(settings.local_storage["base_window_size"])
    game.set_title(settings.WINDOW_TITLE)
    game.set_fps(settings.local_storage["fps"])

    game.add_scene_reference("test-0", RenderTest)

    game.set_current_scene(game.get_scene_reference("test-0"))
    game.mainloop()
