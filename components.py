from typing import Type

import OpenGL.GL as opengl
import OpenGL.GLU as openglu
import glfw as openglfw
import time
import json
import os


# NOTE: Scenes should always be self-contained with
class Scene:
    def __init__(self, window: "Window") -> None:
        self.window = window
        self.is_setup = False

    def get_window(self):
        return self.window

    def setup(self) -> None:
        pass

    def call(self) -> None:
        if self.is_setup:
            self.update()
            self.draw()
        else:
            self.setup()
            self.is_setup = True
            self.call()

    def update(self) -> None:
        pass

    def draw(self) -> None:
        pass


class Window:
    def __init__(self, *args, **kwargs) -> None:
        self.fps = 60
        self.scenes = {}
        self.current_scene = None

        # Make sure OpenGL framework can initialize
        if not openglfw.init():
            raise ImportError("Graphics Library Framework could not initialize")

        # Create graphics window
        self.OPENGL_WINDOW = openglfw.create_window(500, 500, "OpenGL Window", None, None)
        if not self.OPENGL_WINDOW:
            openglfw.terminate()
            raise Exception("Graphics window creation failed.")

        openglfw.make_context_current(self.OPENGL_WINDOW)
        openglfw.set_window_size_callback(self.OPENGL_WINDOW, self.resize_event)
        openglfw.set_window_close_callback(self.OPENGL_WINDOW, self.close_event)

    def set_title(self, title: str) -> None:
        openglfw.set_window_title(self.OPENGL_WINDOW, title)

    def set_fps(self, fps: int) -> None:
        self.fps = fps

    def get_frame_interval(self) -> float:
        return 1 / self.fps

    def set_input_mode(self, input_type: int, option: int):
        openglfw.set_input_mode(self.OPENGL_WINDOW, input_type, option)

    def get_size(self) -> tuple[int, int]:
        return openglfw.get_framebuffer_size(self.OPENGL_WINDOW)

    def set_size(self, size: tuple[int, int]) -> None:
        openglfw.set_window_size(self.OPENGL_WINDOW, size[0], size[1])

    def get_key(self, key: int) -> bool:
        return True if openglfw.get_key(self.OPENGL_WINDOW, key) else False

    def get_cursor_position(self) -> tuple[int, int]:
        return openglfw.get_cursor_pos(self.OPENGL_WINDOW)

    def set_cursor_position(self, x: int, y: int) -> None:
        openglfw.set_cursor_pos(self.OPENGL_WINDOW, x, y)

    def add_scene_reference(self, scene_name: str, scene_reference: Type[Scene]) -> None:
        self.scenes[scene_name] = scene_reference

    def get_scene_reference(self, scene_name: str) -> Type[Scene]:
        return self.scenes[scene_name]

    def set_current_scene(self, scene_reference: Type[Scene]) -> None:
        self.current_scene = scene_reference(self)

    def get_current_scene(self) -> Scene:
        return self.current_scene

    def mainloop(self) -> None:
        while not openglfw.window_should_close(self.OPENGL_WINDOW):
            # Get the time at the start of the frame
            frame_start_time = time.time()

            # Catch graphics window events
            openglfw.poll_events()

            # Render current scene
            self.render()

            # Calculate the time elapsed in this frame
            frame_elapsed_time = time.time() - frame_start_time
            print(f"{round(frame_elapsed_time / self.get_frame_interval() * 100)}%")

            # Sleep for the rest of the frame interval if ahead
            time_to_sleep = max(0.0, self.get_frame_interval() - frame_elapsed_time)
            time.sleep(time_to_sleep)

        openglfw.terminate()

    def resize_event(self, window, width: int, height: int) -> None:
        opengl.glViewport(0, 0, width, height)

    def close_event(self, window) -> None:
        pass

    def render(self) -> None:
        # Clear the color buffer and depth buffer
        opengl.glClear(opengl.GL_COLOR_BUFFER_BIT | opengl.GL_DEPTH_BUFFER_BIT)

        # If the current scene is set then call it
        self.get_current_scene().call()

        # Show current frame
        openglfw.swap_buffers(self.OPENGL_WINDOW)


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
