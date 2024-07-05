import pyautogui # type: ignore
import numpy as np # type: ignore


def controlador_cursor(cx, cy, w, h):
    # Convertir a la resolución de la pantalla
    screen_w, screen_h = pyautogui.size()
    screen_x = np.interp(cx, (0, w), (screen_w, 0))
    screen_y = np.interp(cy, (0, h), (0, screen_h))
    # Mover el puntero
    pyautogui.moveTo(screen_x, screen_y)
