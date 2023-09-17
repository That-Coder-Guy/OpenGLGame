import OpenGL.GL as opengl
import OpenGL.GLU as openglu
import glfw as openglfw
import time
import json
import os


class Scene:
    def __init__(self, window) -> None:
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


class Window:
    def __init__(self, size: tuple = (1000, 800), title: str = "New Window", fps: int = 60) -> None:
        # Make sure OpenGL framework can initialize
        if not openglfw.init():
            raise ImportError("Graphics Library Framework could not initialize")

        # Create graphics window
        self.graphics_window = openglfw.create_window(*size, title, None, None)
        if not self.graphics_window:
            openglfw.terminate()
            raise Exception("Graphics window creation failed.")

        openglfw.make_context_current(self.graphics_window)
        openglfw.set_key_callback(self.graphics_window, self.keyboard_event)
        openglfw.set_window_size_callback(self.graphics_window, self.resize_event)
        openglfw.set_window_close_callback(self.graphics_window, self.close_event)

        self.fps = fps
        self.current_scene = None

    def get_graphics_window(self):
        return self.graphics_window

    def set_frames_per_second(self, fps: int) -> None:
        self.fps = fps

    def get_frame_interval(self) -> float:
        return 1 / self.fps

    def set_current_scene(self, scene: Scene) -> None:
        self.current_scene = scene
        self.get_current_scene().setup()

    def get_current_scene(self) -> Scene:
        return self.current_scene

    def mainloop(self) -> None:
        while not openglfw.window_should_close(self.graphics_window):
            # Get the time at the start of the frame
            frame_start_time = time.time()

            # Catch graphics window events
            openglfw.poll_events()

            # Render current scene
            self.render()

            # Calculate the time elapsed in this frame
            frame_elapsed_time = time.time() - frame_start_time

            # Sleep for the rest of the frame interval if ahead
            time_to_sleep = max(0.0, self.get_frame_interval() - frame_elapsed_time)
            time.sleep(time_to_sleep)

        openglfw.terminate()

    def keyboard_event(self, window, key, scancode, action, mods) -> None:
        # TODO: Figure out how to pass inputs to the current scene
        if key == openglfw.KEY_ESCAPE and action == openglfw.PRESS:
            openglfw.set_window_should_close(window, True)

    def resize_event(self, window, width: int, height: int) -> None:
        opengl.glViewport(0, 0, width, height)
        #openglu.glu
        opengl.glMatrixMode(opengl.GL_PROJECTION)
        opengl.glLoadIdentity()
        openglu.gluPerspective(45, (width / max(1, height)), 0.1, 50.0)
        opengl.glTranslatef(0.0, 0.0, -5)
        opengl.glMatrixMode(opengl.GL_MODELVIEW)
        opengl.glLoadIdentity()

    def close_event(self, window) -> None:
        pass

    def render(self) -> None:
        # Clear the color buffer and depth buffer
        opengl.glClear(opengl.GL_COLOR_BUFFER_BIT | opengl.GL_DEPTH_BUFFER_BIT)

        # If the current scene is set then call it
        if self.get_current_scene() is None:
            raise TypeError("Current scene has not been set")
        else:
            self.get_current_scene().call()

        # Show current frame
        openglfw.swap_buffers(self.graphics_window)


class LocalStorage(dict):
    def __init__(self, filename: str, default: dict):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(filename, "w") as file:
                json.dump(default, file)

        with open(self.filename, "r") as file:
            data = json.load(file)
            super().__init__(data)

    def save_to_disk(self) -> None:
        with open(self.filename, "w") as file:
            json.dump(self, file)
