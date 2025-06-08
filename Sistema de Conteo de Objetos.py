import cv2 as cv
import numpy as np

# Se inicia la captura de video desde la cámara principal (índice 0)
cap = cv.VideoCapture(0)

# Se definen dos rangos de color azul en el espacio HSV para detectar distintos tonos
lower_blue1, upper_blue1 = np.array([100, 150, 50]), np.array([130, 255, 255])
lower_blue2, upper_blue2 = np.array([90, 50, 70]), np.array([110, 150, 255])

# Inicialización de variables de conteo y almacenamiento del estado anterior de los objetos
conteo = 0
obj_prev = []

# Función auxiliar para calcular la distancia euclidiana entre dos puntos
def distancia(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

# Función para determinar si un punto se encuentra dentro de una zona rectangular
def dentro_de_zona(x, y, x1, y1, x2, y2):
    return x1 < x < x2 and y1 < y < y2

# Bucle principal del programa: procesa frame por frame
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Conversión del frame al espacio de color HSV y creación de máscara para color azul
    frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask1 = cv.inRange(frameHSV, lower_blue1, upper_blue1)
    mask2 = cv.inRange(frameHSV, lower_blue2, upper_blue2)
    mask = cv.bitwise_or(mask1, mask2)

    # Se define una zona central de detección mediante un rectángulo rojo
    alto, ancho, _ = frame.shape
    w_rec, h_rec = 250, 250
    cx_frame, cy_frame = ancho // 2, alto // 2
    x1, y1 = cx_frame - w_rec // 2, cy_frame - h_rec // 2
    x2, y2 = cx_frame + w_rec // 2, cy_frame + h_rec // 2
    cv.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # Se detectan contornos en la máscara y se calculan centroides
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    obj_act = []

    for cont in contours:
        area = cv.contourArea(cont)
        if area > 300:  # Filtrado de ruido por área mínima
            x, y, w, h = cv.boundingRect(cont)
            cx = x + w // 2
            cy = y + h // 2
            obj_act.append((cx, cy))
            
    # Se analiza si los objetos actuales ya estaban dentro de la zona en el frame anterior
    new_obj_prev = []

    for cx, cy in obj_act:
        estado = dentro_de_zona(cx, cy, x1, y1, x2, y2)
        afuera = True  # Se asume que el objeto estaba fuera anteriormente

        # Comparación con objetos anteriores para evitar duplicados en el conteo
        for (prev_cx, prev_cy, adentro) in obj_prev:
            if distancia((cx, cy), (prev_cx, prev_cy)) < 40:
                afuera = not adentro
                break

        # Si el objeto entra a la zona por primera vez, se dibuja un punto verde y se aumenta el conteo
        if estado:
            cv.circle(frame, (cx, cy), 5, (0, 255, 0), -1) 
            if afuera:
                conteo += 1
            
        # Se guarda el estado del objeto para el siguiente frame
        new_obj_prev.append((cx, cy, estado))

    obj_prev = new_obj_prev

    # Se muestra el conteo actual sobre la imagen
    cv.putText(frame, f"Conteo: {conteo}", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Visualización del frame resultante
    cv.imshow("VIDEO CAMARA", frame)

    # El bucle finaliza si se presiona la tecla ESC (código ASCII 27)
    if cv.waitKey(1) == 27:
        break

# Al finalizar, se liberan los recursos de la cámara y las ventanas
cap.release()
cv.destroyAllWindows()