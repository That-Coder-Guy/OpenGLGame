import OpenGL.GL as opengl
import OpenGL.GLU as openglu
import glfw as openglfw
import time
import json
import os
import settings


class Scene:
    def __init__(self, window: openglfw._GLFWwindow) -> None:
        self.window = window

    def setup(self) -> None:
        pass

    def update(self) -> None:
        pass

    def draw(self) -> None:
        pass

    def call(self) -> None:
        self.update()
        self.draw()


class TestScene(Scene):
    def __init__(self, window: openglfw._GLFWwindow):
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


class LocalStorage(dict):
    def __init__(self, filename: str, default: dict):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(filename, "w") as file:
                json.dump(default, file)

        with open(self.filename, "r") as file:
            data = json.load(file)
            print(data)
            super().__init__(data)

    def save_to_disk(self) -> None:
        with open(self.filename, "w") as file:
            json.dump(self, file)


storage = LocalStorage("preferences.json", settings.DEFAULT_PREFERENCES)
print(storage["base_window_size"])
storage["base_window_size"] = [100, 100]
storage.save_to_disk()
