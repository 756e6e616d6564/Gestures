import pyautogui # type: ignore
import numpy as np # type: ignore


def controlador_cursor(idv, cTotal, w, h):
    if cTotal is not None:
        x, y = cTotal.x, cTotal.y
        # Convertir a la resolución de la pantalla
        screen_w, screen_h = pyautogui.size()
        screen_x = np.interp(x, (0, w), (w, 0))
        screen_y = np.interp(y, (0, h), (0, h))
        # Mover el puntero
        pyautogui.moveTo(screen_x, screen_y)
    else:
        x, y = 0, 0        
