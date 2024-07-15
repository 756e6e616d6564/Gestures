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
import threading as th #type: ignore
from bin.tst_gesture import *
from multiprocessing import Queue



# Herramientas de mediapipe #
# mpHands = mp.solutions.hands 
# hands = mpHands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5) # TOLERANCIA DE RECONOCIMIENTO #
# mpDraw = mp.solutions.drawing_utils

# Variables de tiempo #
# pTime = 0
# cTime = 0

# puntos = {}  # Diccionario para almacenar las coordenadas de los puntos
# puntosPlus = {}

def run_Gestures(cap, video_width, video_height, max_fps, queue):
    running = True
    while running: 
        idv, lmv, success, running = gesture_main(running, cap, video_width, video_height, max_fps, queue)
        queue.put((idv, lmv, success, running))

def run_Cursor(idv, lmv,video_width, video_height, running):
    while running:
        controlador_cursor(idv, lmv, video_width, video_height)

#proceso_gestos = th.Thread(target=run_Gestures, args=(cap, video_width, video_height, max_fps))

if __name__ == '__main__' :
        
    running = True
    max_fps = 12

    #  Asignación de variables para Gesture #

    cap = cv2.VideoCapture(0) # 0 para la cámara por defecto, ir subiendo números para otras cámaras 

    # 320x240 // 960x720
    video_width = 600
    video_height = 400

    queue = Queue()
    proceso_gestos = th.Thread(target=run_Gestures, args=(cap, video_width, video_height, max_fps, queue))
    proceso_gestos.start()

    # Recuperar resultados de la Queue
    idv, lmv, success, running = queue.get()
    #run_Cursor(proceso_gestos.idv, proceso_gestos.lmv)
    proceso_cursor = th.Thread(target=run_Cursor, args=(idv, lmv, video_width, video_height, running))
    proceso_cursor.start()

    proceso_gestos.join()  # Esperar a que el hilo termine
    proceso_cursor.join()

    

else: 
    print("Error estructural")