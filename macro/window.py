import time
from utils import ScreenCoordinates
from win32 import win32gui, win32process
from win32.lib import win32con

class Window:
    def __init__(self, hwnd: int) -> None:
        self.hwnd = hwnd
        _, self.pid = win32process.GetWindowThreadProcessId(self.hwnd)
    
    @staticmethod
    def get_current():
        return Window(win32gui.GetForegroundWindow())

    def get_hwnd(self) -> int:
        return self.hwnd

    def get_pid(self) -> int:
        return self.pid
    
    def get_title(self) -> str:
        return win32gui.GetWindowText(self.hwnd)
    
    def set_title(self, title: str) -> None:
        win32gui.SetWindowText(self.hwnd, title)
    
    def set_position(self, *, coordinates: ScreenCoordinates, center: bool = True):
        x, y = coordinates.__tuple__()
        win_x, win_y, girth, length = win32gui.GetWindowRect(self.hwnd)
        width = girth - win_x
        height = length - win_y
        if center:
            x, y = ScreenCoordinates(x - (width / 2), y - (height / 2)).__tuple__()
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_NOTOPMOST, x, y, width, height, win32con.SWP_ASYNCWINDOWPOS)

time.sleep(1)
Window.get_current().set_position(coordinates=ScreenCoordinates.center(), center=False)
