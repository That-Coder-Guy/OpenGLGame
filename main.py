import sys
import time
import settings
import components
import OpenGL.GL as opengl
import OpenGL.GLU as openglu
import glfw as openglfw

class TestScene(components.Scene):
    def __init__(self, window):
        super().__init__(window=window)
        self.cube_vertices = ((1, 1, 1), (1, 1, -1), (1, -1, -1), (1, -1, 1),
                              (-1, 1, 1), (-1, -1, -1), (-1, -1, 1), (-1, 1, -1))
        self.cube_edges = ((0, 1), (0, 3), (0, 4), (1, 2), (1, 7), (2, 5),
                           (2, 3), (3, 6), (4, 6), (4, 7), (5, 6), (5, 7))
        self.cube_quads = ((0, 3, 6, 4), (2, 5, 6, 3), (1, 2, 5, 7),
                           (1, 0, 4, 7), (7, 4, 6, 5), (2, 3, 0, 1))

    def setup(self) -> None:
        width, height = openglfw.get_framebuffer_size(self.window)
        openglu.gluPerspective(45, (width / height), 0.1, 50.0)
        opengl.glTranslatef(0.0, 0.0, -5)

    def update(self) -> None:
        opengl.glRotatef(1, 1, 1, 1)

    def draw(self) -> None:
        opengl.glBegin(opengl.GL_LINES)
        for edge in self.cube_edges:
            for vertex in edge:
                opengl.glVertex3fv(self.cube_vertices[vertex])
        opengl.glEnd()


class GameWindow(components.Window):
    def __init__(self) -> None:
        super().__init__(size=settings.local_storage["base_window_size"],
                         title=settings.WINDOW_TITLE,
                         fps=settings.local_storage["fps"])
        # Initialize scenes
        self.scene1 = TestScene(self.get_graphics_window())

        # Set initial scene
        self.set_current_scene(self.scene1)

    def keyboard_event(self, window, key, scancode, action, mods) -> None:
        super().keyboard_event(window, key, scancode, action, mods)


if __name__ == "__main__":
    game = GameWindow()
    game.mainloop()
