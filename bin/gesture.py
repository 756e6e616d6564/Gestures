import os
import time
import cv2 # type: ignore
import mediapipe as mp # type: ignore
import numpy as np # type: ignore

running = True
max_fps = 20

def stop_program():
    global running
    running = False

def main_loop():
    global running, pTime, cTime
    while running:

        
        success, img = cap.read()
        img = cv2.flip(img, 1) # Voltear la imagen
        
        frame = cv2.resize(img, (video_width, video_height)) # Redimensionar la imagen
        img = frame

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
        results = hands.process(img) 
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
       
        conexiones = [
                    (0, 1), (1, 2), (2, 3), (3, 4),  # Pulgar
                    (0, 5), (5, 6), (6, 7), (7, 8),  # Índice
                    #DEBUGGING
                    (1, 5), (2, 5), (4, 8)
                    ]

        if results.multi_hand_landmarks: # Si se detecta una mano

            for handLms in results.multi_hand_landmarks: # Por cada mano detectada

                for id, lm in enumerate(handLms.landmark):
                    
                    h, w, c = img.shape # Obtener el alto, ancho y canales de la imagen
                    x = lm.x
                    y = lm.y

                    x = round(x, 6)
                    y = round(y, 6)
                    
                    print(h,'Height  ', w,'Width  ', x,'lmX  ', y,'lmY')
                    cx, cy = int(x*w), int(y*h)

                    # Dibujar puntos en la imagen #
                    if (id == 4) or (id == 8) or (id == 0) or (id == 30):
                        #print(id, cx, cy) 
                        pass
                    puntos[id] = (cx, cy)

                    if id == 0 or id == 1 or id == 5: # Punto de la muñeca
                        cv2.circle(img, (cx, cy), 6, (0, 0, 255), cv2.FILLED)
                    
                    elif id == 8 or id == 7 or id == 6: # Punto de la punta del dedo índice
                        cv2.circle(img, (cx, cy), 4, (0, 255, 0), cv2.FILLED)
                    
                    elif id == 4 or id == 3 or id == 2: # Punto de la punta del dedo pulgar
                        cv2.circle(img, (cx, cy), 4, (255, 0, 0), cv2.FILLED)
                        # Puntos muertos #
                    else:
                        cv2.circle(img, (cx, cy), 2, (0, 0, 0), cv2.FILLED)              

                    
                    # Procesa el dedo pulgar con el índice, y genera un punto extra en el medio de ambos dedos #
                    if 8 in puntos:
                        cx, cy = puntos[8]  # Extracción de coordenadas para el índice #
                        
                        cx2, cy2 = puntos[4]  # Extracción de coordenadas para el pulgar #

                        # Calcula la distancia entre los dos puntos
                        distancia = np.sqrt((cx - cx2)**2 + (cy - cy2)**2)

                        umbral = 25  #TOLERANCIA DE DEDOS JUNTOS ############################<<<<<<<<<

                        # Si la distancia es menor que el umbral, crea un nuevo punto
                        if distancia < umbral:
                            # Calcula el punto medio entre los dos puntos
                            nx = (cx + cx2) // 2
                            ny = (cy + cy2) // 2

                            id = "30"
                            puntos[id] = (nx, ny)
                                                        
                            # Dibuja un nuevo círculo en el punto medio
                            cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)

                        cv2.putText(img, str(puntos[8]), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(img, str(puntos[4]), (cx2, cy2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(img, str(round(distancia, 2)), (((cx + cx2) // 2), ((cy + cy2) // 2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                            
                    else:
                        print("El punto 8 no ha sido detectado")

                    for start, end in conexiones:
                        # Obtén las coordenadas de inicio y fin de la conexión
                        start_lm = handLms.landmark[start]
                        end_lm = handLms.landmark[end]
                        start_x, start_y = int(start_lm.x * w), int(start_lm.y * h)
                        end_x, end_y = int(end_lm.x * w), int(end_lm.y * h)

                        # Dibuja la línea entre los puntos
                        cv2.line(img, (start_x, start_y), (end_x, end_y), (255, 255, 255), 1)
                    

                
    #######################################################################
                    
        
        # Guarda los parámetros en un archivo txt
        try:
            with open('data/Benchmark Data/hardData/fpsLog.txt', 'a') as file:
                file.write(f'{fps}\t{cTime}\n')
        except:
            with open('../data/Benchmark Data/hardData/fpsLog.txt', 'a') as file:
                file.write(f'{fps}\t{cTime}\n')

        if fps <= 10: ## FPS EN PANTALLA
            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (10, 10, 10), 3)
        elif fps < 10:
            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
        elif fps < 20:
            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        elif fps < 30:
            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)



        cv2.imshow("GEstuRE", img)

        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('GEstuRE', cv2.WND_PROP_VISIBLE) < 1: # Cerrar la ventana con la tecla 'q' o el botón de cerrar
            stop_program()
            break            
        if success == False:
            break
    return id, lm
    
    

###### DECLARACIÓN DE VARIABLES #####



# Inicializar la cámara
cap = cv2.VideoCapture(0) # 0 para la cámara por defecto, ir subiendo números para otras cámaras ///  320x240 // 960x720

video_width = 600
video_height = 400

# Herramientas de mediapipe #
mpHands = mp.solutions.hands 
hands = mpHands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5) # TOLERANCIA DE RECONOCIMIENTO #
mpDraw = mp.solutions.drawing_utils

# Variables de tiempo #
pTime = 0
cTime = 0


puntos = {}  # Diccionario para almacenar las coordenadas de los puntos
puntosPlus = {}

if __name__ == '__main__':
    if os.path.exists('data/Benchmark Data/hardData/fpsLog.txt'):
        os.remove('data/Benchmark Data/hardData/fpsLog.txt')

    main_loop()
    cap.release()
    cv2.destroyAllWindows()
    print('Programa finalizado')
