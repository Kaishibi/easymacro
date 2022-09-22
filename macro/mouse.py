from .utils import ScreenCoordinates
from win32 import win32gui, win32api
from win32.lib import win32con

class MouseButtons:
    def _register(down, up) -> dict:
        return {"down": down, "up": up}

    Left = _register(win32con.MOUSEEVENTF_LEFTDOWN, win32con.MOUSEEVENTF_LEFTUP)
    Right = _register(win32con.MOUSEEVENTF_RIGHTDOWN, win32con.MOUSEEVENTF_RIGHTUP)
    Middle = _register(win32con.MOUSEEVENTF_MIDDLEDOWN, win32con.MOUSEEVENTF_MIDDLEUP)
    Extra = _register(win32con.MOUSEEVENTF_XDOWN, win32con.MOUSEEVENTF_XUP)

class Mouse:
    def __init__(self) -> None:
        self.clipped = False
    
    def get_position(self) -> ScreenCoordinates:
        x, y = win32gui.GetCursorPos()
        return ScreenCoordinates(x, y)
    
    def set_position(self, coordinates: ScreenCoordinates) -> None:
        x, y = coordinates.__tuple__()
        win32api.SetCursorPos((x, y))

    def clip(self, *, coordinates: ScreenCoordinates, coordinates2: ScreenCoordinates = None, set_position: bool = False) -> None:
        if coordinates2 is None:
            coordinates2 = coordinates
        x, y = coordinates.__tuple__()
        x2, y2 = coordinates2.__tuple__()
        win32api.ClipCursor((x - 1, y - 1, x2 + 1, y2 + 1))
        if set_position:
            self.set_position(ScreenCoordinates((x + x2) / 2, (y + y2) / 2))
        self.clipped = True
    
    def unclip(self) -> None:
        if not self.clipped:
            return
        win32api.ClipCursor((0, 0, 0, 0))
        self.clipped = False

    def click_down(self, *, coordinates: ScreenCoordinates, button: MouseButtons) -> None:
        if type(button) is not dict:
            raise TypeError("Argument 'button' cannot be the MouseButtons class itself.")

        self.clip(coordinates=coordinates, set_position=True)
        win32api.mouse_event(button["down"] | win32con.MOUSEEVENTF_ABSOLUTE, 0, 0)
        self.unclip()
    
    def click_up(self, *, coordinates: ScreenCoordinates, button: MouseButtons) -> None:
        if type(button) is not dict:
            raise TypeError("Argument 'button' cannot be the MouseButtons class itself.")

        self.clip(coordinates=coordinates, set_position=True)
        win32api.mouse_event(button["up"] | win32con.MOUSEEVENTF_ABSOLUTE, 0, 0)
        self.unclip()
    
    def click(self, *, coordinates: ScreenCoordinates, button: MouseButtons, reset_position: bool = False) -> None:
        initial_pos = self.get_position()
        self.click_down(coordinates=coordinates, button=button)
        self.click_up(coordinates=coordinates, button=button)
        if reset_position:
            self.set_position(initial_pos)
