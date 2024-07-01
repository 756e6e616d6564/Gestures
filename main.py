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

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
        results = hands.process(imgRGB) 

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        if results.multi_hand_landmarks: # Si se detecta una mano
            for handLms in results.multi_hand_landmarks: # Por cada mano detectada
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS) # Dibujar los puntos de la mano y las conexiones entre ellos
                for id, lm in enumerate(handLms.landmark): 
                    h, w, c = img.shape # Obtener el alto, ancho y canales de la imagen
                    cx, cy = int(lm.x*w), int(lm.y*h) 
                    print(id, cx, cy) 
                    puntos[id] = (cx, cy)

                    if id == 0: # Punto de la muñeca
                        cv2.circle(img, (cx, cy), 15, (0, 0, 153), cv2.FILLED)
                    
                    if id == 8: # Punto de la punta del dedo
                        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                    
                    if id == 4: # Punto de la punta del dedo
                        cv2.circle(img, (cx, cy), 15, (255, 128, 0), cv2.FILLED)

                    if id == 12: # Punto de la punta del dedo
                        cv2.circle(img, (cx, cy), 15, (153, 0, 0), cv2.FILLED)
                    
                    #TEST###############################
                    if 8 in puntos:
                        cx, cy = puntos[8]  # Coordenadas para el punto con id=8
                        # Aquí puedes continuar con tu lógica, como crear un nuevo punto si id=8 e id=4 están "juntos"
                          
                        cx2, cy2 = puntos[4]  # Coordenadas para el punto con id=4

                        # Calcula la distancia entre los dos puntos
                        distancia = np.sqrt((cx - cx2)**2 + (cy - cy2)**2)

                        # Umbral para determinar si los puntos están "juntos"
                        umbral = 20  # Ajusta este valor según sea necesario

                        # Si la distancia es menor que el umbral, crea un nuevo punto
                        if distancia < umbral:
                            # Calcula el punto medio entre los dos puntos
                            punto_x = (cx + cx2) // 2
                            punto_y = (cy + cy2) // 2

                            idPunto_generado = "30"
                            puntos[idPunto_generado] = (punto_x, punto_y)
                                                        
                            # Dibuja un nuevo círculo en el punto medio
                            cv2.circle(img, (punto_x, punto_y), 15, (0, 255, 0), cv2.FILLED)
                            print(idPunto_generado, punto_x, punto_y)
                    else:
                        print("El punto con id=8 no ha sido detectado aún.")
                                        # Suponiendo que tienes las coordenadas (cx, cy) para id=8 y (cx2, cy2) para id=4
                   
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
cap = cv2.VideoCapture(1) # 0 para la cámara por defecto, ir subiendo números para otras cámaras

# Inicializar las herramientas de mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands()
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
