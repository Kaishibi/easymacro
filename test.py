import time
from macro import Window

# time.sleep(1)
test = Window.find_by_title("File Explorer").is_active()
print(test)