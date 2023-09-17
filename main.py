import sys
import time
import settings
import components
import OpenGL.GL as opengl
import glfw as openglfw


if not openglfw.init():
    raise ImportError("Graphics Library Framework could not initialize")


#opengl.glViewport(0, 0, *event.size)
#opengl.glMatrixMode(opengl.GL_PROJECTION)
#opengl.glLoadIdentity()
#openglu.gluPerspective(45, (event.size[0] / event.size[1]), 0.1, 50.0)
#opengl.glTranslatef(0.0, 0.0, -5)
#opengl.glMatrixMode(opengl.GL_MODELVIEW)
#opengl.glLoadIdentity()


class GameWindow:
    def __init__(self) -> None:

        # Create graphics window
        self.window = openglfw.create_window(*settings.window_base_size, settings.WINDOW_TITLE, None, None)
        if not self.window:
            openglfw.terminate()
            raise Exception("Graphics window creation failed.")

        openglfw.make_context_current(self.window)
        openglfw.set_key_callback(self.window, self.handle_keyboard_event)

        self.test = components.Test(self.window)

    def mainloop(self) -> None:
        frame_interval = 1.0 / 60
        while not openglfw.window_should_close(self.window):
            frame_start_time = time.time()

            # Your main loop logic and rendering code go here
            openglfw.poll_events()
            self.render()

            # Calculate the time elapsed in this frame
            frame_elapsed_time = time.time() - frame_start_time
            time_to_sleep = max(0, frame_interval - frame_elapsed_time)
            print(time_to_sleep, frame_interval)
            time.sleep(time_to_sleep)
        openglfw.terminate()

    def handle_keyboard_event(self, window, key, scancode, action, mods) -> None:
        if key == openglfw.KEY_ESCAPE and action == openglfw.PRESS:
            openglfw.set_window_should_close(window, True)

    def render(self) -> None:
        # Clear the color buffer and depth buffer
        opengl.glClear(opengl.GL_COLOR_BUFFER_BIT | opengl.GL_DEPTH_BUFFER_BIT)
        self.test.run()
        openglfw.swap_buffers(self.window)


if __name__ == "__main__":
    game = GameWindow()
    game.mainloop()
