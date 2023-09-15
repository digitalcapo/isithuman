import cv2
import random
import time

def dibujar_analisis(frame, porcentaje, color_barra):
    height, width, _ = frame.shape
    bar_width = int(width * 0.6)
    bar_start_x = int((width - bar_width) / 2)
    bar_start_y = int(height * 0.5) - 10  # Centrado en la altura
    bar_height = 20

    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size = cv2.getTextSize("ANALIZANDO........", font, 1, 2)[0]
    text_x = (width - text_size[0]) // 2
    text_y = int(height * 0.5) - 40
    #cv2.putText(frame, "ANALIZANDO........", (text_x, text_y), font, 1, color_barra, 2, cv2.LINE_AA)
    cv2.rectangle(frame, (bar_start_x, bar_start_y), (bar_start_x + bar_width, bar_start_y + bar_height), color_barra, 2)
    filled_width = int((bar_width - 2) * porcentaje / 100)
    cv2.rectangle(frame, (bar_start_x + 1, bar_start_y + 1), (bar_start_x + filled_width, bar_start_y + bar_height - 1), color_barra, -1)

def generar_mac_address():
    return ':'.join(['%02x' % random.randint(0, 255) for _ in range(6)])

def agregar_stream_datos(frame):
    height, width, _ = frame.shape
    start_y = 4
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 255, 255)

    for _ in range(800):  # Numero arbitrario de direcciones MAC
        mac = generar_mac_address()
        text_size = cv2.getTextSize(mac, font, 0.5, 1)[0]
        cv2.putText(frame, mac, (width - text_size[0] - 10, start_y), font, 0.5, color, 1, cv2.LINE_AA)
        start_y += text_size[1] + 4

def detectar_rostros(video_capture):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    colores = [(255, 0, 255), (0, 255, 0), (255, 255, 255)]  
    color_index = 2

    analizando = False
    porcentaje = 0
    start_analisis = None
    mostrando_resultado = False
    tiempo_resultado = None
    resultado = ""
    tiempo_espera = None
    img_bw = None

    while True:
        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Corner processing
        corner_w = 480
        corner_h = 480
        corner_x, corner_y = 10, frame.shape[0] - corner_h - 10

        if img_bw is not None:
            img_resized = cv2.resize(img_bw, (corner_w, corner_h))
            color_resized = cv2.cvtColor(img_resized, cv2.COLOR_GRAY2BGR)
            frame[corner_y:corner_y+corner_h, corner_x:corner_x+corner_w] = color_resized
            cv2.rectangle(frame, (corner_x-10, corner_y-10), (corner_x+corner_w+10, corner_y+corner_h+10), (255, 255, 255), 8)

        if len(faces) > 0 and not mostrando_resultado:
            (x, y, w, h) = faces[0]
            img_bw = cv2.cvtColor(frame[y:y+h, x:x+w], cv2.COLOR_BGR2GRAY)
            cv2.rectangle(frame, (x, y), (x+w, y+h), colores[color_index], 1)

            if not analizando and (tiempo_espera is None or time.time() - tiempo_espera > random.randint(5, 7)):
                analizando = True
                porcentaje = 0
                start_analisis = time.time()

        agregar_stream_datos(frame)
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def main():
    global video_capture
    video_capture = cv2.VideoCapture(3)
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Cambiar resolución a 640x480 para una relación 4:3
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    detectar_rostros(video_capture)
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
