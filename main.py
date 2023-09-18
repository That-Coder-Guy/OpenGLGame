import math
import random
import settings
import components
import OpenGL.GL as opengl
import OpenGL.GLU as openglu
import glfw as openglfw


class TestScene(components.Scene):
    def __init__(self, window):
        super().__init__(window=window)
        self.cube_vertices = ((0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 0),
                              (1, 0, 0), (1, 1, 1), (1, 1, 0), (1, 0, 1))
        self.cube_edges = ((0, 1), (0, 3), (0, 4), (1, 2), (1, 7), (2, 5),
                           (2, 3), (3, 6), (4, 6), (4, 7), (5, 6), (5, 7))
        #self.cube_faces = ((0, 3, 6, 4), (2, 5, 6, 3), (1, 2, 5, 7),
        #                   (1, 0, 4, 7), (7, 4, 6, 5), (2, 3, 0, 1))

        self.cube_faces = ((0, 3, 6, 4), (2, 5, 6, 3), (7, 5, 2, 1),
                           (1, 0, 4, 7), (7, 4, 6, 5), (2, 3, 0, 1))
        self.position = [0.0, 0.0, 0.0]
        self.angle = [0.0, 0.0, 0.0]

    def setup(self) -> None:
        width, height = openglfw.get_framebuffer_size(self.window)

        openglfw.set_input_mode(self.window, openglfw.CURSOR, openglfw.CURSOR_DISABLED)
        openglfw.set_cursor_pos(self.window, round(width / 2), round(height / 2))

        # Enable back-face culling
        opengl.glEnable(opengl.GL_CULL_FACE)
        opengl.glCullFace(opengl.GL_BACK)

        # NOTE: Remember that enabling the depth buffer hides unneeded faces instead
        #       of not drawing that in the first place
        opengl.glEnable(opengl.GL_DEPTH_TEST)

    def update(self) -> None:
        width, height = openglfw.get_framebuffer_size(self.window)

        cursor_velocity = self.get_cursor_velocity()
        self.angle[0] = (self.angle[0] + cursor_velocity[0] / 8) % 360
        self.angle[1] = max(min(90.0, self.angle[1] + cursor_velocity[1] / 8), -90.0)

        self.set_cursor_to_center()
        if openglfw.get_key(self.window, openglfw.KEY_W):
            self.position[0] -= math.sin((self.angle[0] / 180) * math.pi) * 0.1
            self.position[2] += math.cos((self.angle[0] / 180) * math.pi) * 0.1
        if openglfw.get_key(self.window, openglfw.KEY_S):
            self.position[0] += math.sin((self.angle[0] / 180) * math.pi) * 0.1
            self.position[2] -= math.cos((self.angle[0] / 180) * math.pi) * 0.1
        if openglfw.get_key(self.window, openglfw.KEY_A):
            self.position[0] += math.cos((self.angle[0] / 180) * math.pi) * 0.1
            self.position[2] += math.sin((self.angle[0] / 180) * math.pi) * 0.1
        if openglfw.get_key(self.window, openglfw.KEY_D):
            self.position[0] -= math.cos((self.angle[0] / 180) * math.pi) * 0.1
            self.position[2] -= math.sin((self.angle[0] / 180) * math.pi) * 0.1

        if openglfw.get_key(self.window, openglfw.KEY_SPACE):
            self.position[1] -= 0.1
        if openglfw.get_key(self.window, openglfw.KEY_LEFT_SHIFT):
            self.position[1] += 0.1

        opengl.glLoadIdentity()
        opengl.glMatrixMode(opengl.GL_PROJECTION)
        openglu.gluPerspective(45, (width / max(1, height)), 0.1, 50.0)
        opengl.glRotatef(self.angle[1], True, False, False)
        opengl.glRotatef(self.angle[0], False, True, False)
        opengl.glTranslatef(*self.position)

    def get_cursor_velocity(self) -> tuple[int, int]:
        width, height = openglfw.get_framebuffer_size(self.window)
        mouse_x, mouse_y = openglfw.get_cursor_pos(self.window)
        return int(mouse_x - width / 2), int(mouse_y - height / 2)

    def set_cursor_to_center(self) -> None:
        width, height = openglfw.get_framebuffer_size(self.window)
        openglfw.set_cursor_pos(self.window, round(width / 2), round(height / 2))

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




class GameWindow(components.Window):
    def __init__(self) -> None:
        super().__init__(size=settings.local_storage["base_window_size"],
                         title=settings.WINDOW_TITLE,
                         fps=settings.local_storage["fps"])
        # Initialize scenes
        self.scene1 = TestScene(self.get_graphics_window())

        # Set initial scene
        self.set_current_scene(self.scene1)


if __name__ == "__main__":
    game = GameWindow()
    game.mainloop()
