import cv2
import numpy as np
import random

# Función ficticia para clasificar comida
def clasificar_comida(imagen):
    comidas = ["Pizza", "Hamburguesa", "Sushi", "Pasta", "Ensalada", "Helado"]
    resultados = []

    # Añadimos cuadraditos aleatoriamente para el ejemplo
    for _ in range(5):
        x = random.randint(0, imagen.shape[1] - 1)
        y = random.randint(0, imagen.shape[0] - 1)
        comida = random.choice(comidas)
        resultados.append((x, y, comida))
    
    return resultados

# Capturar imagen de la cámara
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()

if ret:
    clasificaciones = clasificar_comida(frame)

    for x, y, comida in clasificaciones:
        cv2.rectangle(frame, (x, y), (x + 100, y + 50), (0, 255, 0), 2)
        cv2.putText(frame, comida, (x, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow('Clasificador de comida', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
