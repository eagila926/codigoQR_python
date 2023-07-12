import cv2
from pyzbar import pyzbar
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Función para leer el código QR
def leer_codigo_qr():
    # Inicializar la cámara
    cap = cv2.VideoCapture(0)

    while True:
        # Leer un fotograma de la cámara
        _, frame = cap.read()

        # Decodificar los códigos QR presentes en el fotograma
        codigos_qr = pyzbar.decode(frame)

        # Procesar los códigos QR encontrados
        for codigo_qr in codigos_qr:
            # Obtener el contenido del código QR
            contenido = codigo_qr.data.decode("utf-8")

            # Obtener la hora actual
            hora_lectura = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Registrar el código QR y la hora de lectura en la base de datos
            # registrar_lectura_qr(contenido, hora_lectura)

            # Mostrar el contenido del código QR en la consola
            print("Contenido del código QR:", contenido)
            print("Hora de lectura",hora_lectura)

        # Mostrar el fotograma
        cv2.imshow("Lector de código QR", frame)

        # Salir si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Liberar los recursos
    cap.release()
    cv2.destroyAllWindows()

# Función para registrar la lectura del código QR en la base de datos
def registrar_lectura_qr(contenido, hora_lectura):
    try:
        # Conectar a la base de datos MySQL
        conexion = mysql.connector.connect(
            host="localhost",
            database="nombre_base_de_datos",
            user="nombre_usuario",
            password="contraseña"
        )

        if conexion.is_connected():
            # Insertar los datos en la tabla de la base de datos
            cursor = conexion.cursor()
            consulta = "INSERT INTO lecturas_qr (contenido, hora_lectura) VALUES (%s, %s)"
            datos = (contenido, hora_lectura)
            cursor.execute(consulta, datos)
            conexion.commit()
            cursor.close()

    except Error as e:
        print("Error al conectar a la base de datos:", e)

    finally:
        if conexion.is_connected():
            conexion.close()
            print("Conexión a la base de datos cerrada.")

# Llamar a la función para leer el código QR
leer_codigo_qr()
