import sys
import ctypes
import win32api
from pywintypes import DEVMODEType, error

class ScreenRes(object):
    @classmethod
    def set(cls, width=None, height=None, depth=32):
        if width and height:
            if not depth:
                depth = 32
            mode = win32api.EnumDisplaySettings()
            mode.PelsWidth = width
            mode.PelsHeight = height
            mode.BitsPerPel = depth
            
            win32api.ChangeDisplaySettings(mode, 0)
        else:
            win32api.ChangeDisplaySettings(None, 0)
            
        
    @classmethod
    def get(cls):
        user32 = ctypes.windll.user32
        screensize = (
            user32.GetSystemMetrics(0),
            user32.GetSystemMetrics(1),
            )
        return screensize

    @classmethod
    def get_modes(cls):
        modes = []
        i = 0
        try:
            while True:
                mode = win32api.EnumDisplaySettings(None, i)
                modes.append((
                    int(mode.PelsWidth),
                    int(mode.PelsHeight),
                    int(mode.BitsPerPel),
                    ))
                i += 1
        except error:
            pass
            
        return modes


if __name__ == '__main__':
    # print('Primary screen resolution: {}x{}'.format(*ScreenRes.get()))
    # print(ScreenRes.get_modes())
    ScreenRes.set(1366, 768)