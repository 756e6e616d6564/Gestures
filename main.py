import os
import time
import cv2 # type: ignore
import mediapipe as mp # type: ignore
import numpy as np # type: ignore

running = True

def stop_program():
    global running
    running = False

def main_loop():
    global running, pTime, cTime
    while running:
        success, img = cap.read()

        frame = cv2.resize(img, (video_width, video_height)) # Redimensionar la imagen

        img = frame

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
        results = hands.process(img) 
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        conexiones_permitidas = [
                                (0, 1), (1, 2), (2, 3), (3, 4),  # Pulgar
                                (0, 5), (5, 6), (6, 7), (7, 8)  # Índice
                                ]

        if results.multi_hand_landmarks: # Si se detecta una mano
            for handLms in results.multi_hand_landmarks: # Por cada mano detectada
                #mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS) # Dibujar los puntos de la mano y las conexiones entre ellos
                
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape # Obtener el alto, ancho y canales de la imagen
                    cx, cy = int(lm.x*w), int(lm.y*h) 
                    print(id, cx, cy) 
                    puntos[id] = (cx, cy)

                    if id == 0: # Punto de la muñeca
                        cv2.circle(img, (cx, cy), 10, (0, 0, 153), cv2.FILLED)
                    
                    elif id == 8: # Punto de la punta del dedo
                        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                    
                    elif id == 4: # Punto de la punta del dedo
                        cv2.circle(img, (cx, cy), 5, (255, 128, 0), cv2.FILLED)
                    
                    #TEST# Procesa el dedo pulgar con el índice, y genera un punto extra en el medio de ambos dedos
                    if 8 in puntos:
                        cx, cy = puntos[8]  # Coordenadas para el punto con id=8
                        
                        cx2, cy2 = puntos[4]  # Coordenadas para el punto con id=4

                        # Calcula la distancia entre los dos puntos
                        distancia = np.sqrt((cx - cx2)**2 + (cy - cy2)**2)

                        # Umbral para determinar si los puntos están "juntos"
                        umbral = 25  # Ajusta este valor según sea necesario (TOLERANCIAA) ############################<<<<<<<<<

                        # Si la distancia es menor que el umbral, crea un nuevo punto
                        if distancia < umbral:
                            # Calcula el punto medio entre los dos puntos
                            punto_x = (cx + cx2) // 2
                            punto_y = (cy + cy2) // 2

                            idPunto_generado = "30"
                            puntos[idPunto_generado] = (punto_x, punto_y)
                                                        
                            # Dibuja un nuevo círculo en el punto medio
                            cv2.circle(img, (punto_x, punto_y), 5, (0, 255, 0), cv2.FILLED)
                            print(idPunto_generado, punto_x, punto_y)
                    else:
                        print("El punto con id=8 no ha sido detectado aún.")
                                        # Suponiendo que tienes las coordenadas (cx, cy) para id=8 y (cx2, cy2) para id=4

                    for start, end in conexiones_permitidas:
                        # Obtén las coordenadas de inicio y fin de la conexión
                        start_lm = handLms.landmark[start]
                        end_lm = handLms.landmark[end]
                        start_x, start_y = int(start_lm.x * w), int(start_lm.y * h)
                        end_x, end_y = int(end_lm.x * w), int(end_lm.y * h)

                        # Dibuja la línea entre los puntos
                        cv2.line(img, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
                    ########################################
                    
        
        # Guarda los parámetros en un archivo txt
        with open('parameters.txt', 'a') as file:
            file.write(f'{fps}\t{cTime}\n')
        
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3) # Mostrar los FPS en la pantalla
        cv2.imshow("GEstuRE", img)

        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('GEstuRE', cv2.WND_PROP_VISIBLE) < 1: # Cerrar la ventana con la tecla 'q' o el botón de cerrar
            stop_program()
            break            

    if not success:
        print("Ignoring empty camera frame.")
        return


# Inicializar la cámara
cap = cv2.VideoCapture(1) # 0 para la cámara por defecto, ir subiendo números para otras cámaras ///  320x240 // 960x720
video_width = 960
video_height = 720




# Inicializar las herramientas de mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5) 
mpDraw = mp.solutions.drawing_utils

# Inicializar variables de tiempo
pTime = 0
cTime = 0


puntos = {}  # Diccionario para almacenar las coordenadas de los puntos


if __name__ == '__main__':
    if os.path.exists('parameters.txt'):
            os.remove('parameters.txt')
    main_loop()
    cap.release()
    cv2.destroyAllWindows()
    print('Programa finalizado')
