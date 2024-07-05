import os
import time
import cv2 # type: ignore
import mediapipe as mp # type: ignore
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from multiprocessing import Process, Queue
from bin.gesture import *
from ve.tools.graphCreator import *
from bin.cursor import *
import pyautogui # type: ignore

w, h = 0, 0

def get_screen_resolution():
    global w, h 
    screen_info = pyautogui.size()
    w, h = int(screen_info['screen_width']), int(screen_info['screen_height'])                                  
    w = int(w)
    h = int(h)
    return w, h

def backgroud_task(queue):
    queue.put(main_loop())
    x, y = main_loop()
    controlador_cursor(x, y, w, h)
    

if __name__ == '__main__':
    get_screen_resolution()
    queue = Queue()
    p = Process(target=backgroud_task, args=(queue,))
    p.start()
    p.join()
    print(queue.get())

createGraph()
    