import pyautogui
import os
from datetime import datetime

class ScreenCapture:
    def __init__(self, save_path="prints_erro"):
        self.save_path = save_path
        if not os.path.exists(save_path):
            os.makedirs(save_path)

    def print_momento_erro(self, nome_empresa, tipo):
        filename = f"{tipo}_{nome_empresa}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        file_path = os.path.join(self.save_path, filename)
        screenshot = pyautogui.screenshot()
        screenshot.save(file_path)
        
