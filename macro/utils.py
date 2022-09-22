from win32 import win32api

class ScreenCoordinates:
    def __init__(self, x: int, y: int) -> None:
        self.x = int(round(x, 0))
        self.y = int(round(y, 0))
    
    @staticmethod
    def center(*, monitor: int = 0):
        monitors = win32api.EnumDisplayMonitors()
        if len(monitors) - 1 > monitor or monitor < 0:
            raise TypeError("Invalid monitor.")
        dimensions = monitors[monitor][2]
        _, _, x, y = dimensions
        return ScreenCoordinates(x / 2, y / 2)

    def __tuple__(self) -> tuple:
        return self.x, self.y
    
    def __dict__(self) -> dict:
        return {"x": self.x, "y": self.y}
    
    def __str__(self) -> str:
        return f"{self.x}:{self.y}"
