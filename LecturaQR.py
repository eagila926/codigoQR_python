import cv2
from pyzbar import pyzbar
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import time

# Función para leer el código QR
def leer_codigo_qr():
    # Inicializar la cámara
    cap = cv2.VideoCapture(0)

    while True:
        # Leer un fotograma de la cámara
        _, frame = cap.read()

        #ubicar el codigo QR
        cv2.putText(frame, 'Localizar codigo QR', (160,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2)

        #Ubicar rectangulo en las zona
        cv2.rectangle(frame, (170,100),(470,400),(0,255,0),2)

        # Decodificar los códigos QR presentes en el fotograma
        codigos_qr = pyzbar.decode(frame)

        # Procesar los códigos QR encontrados
        for codigo_qr in codigos_qr:
            # Obtener el contenido del código QR
            contenido = codigo_qr.data.decode("utf-8")
            

            #Convertir el contenido en estring
            dataqr= str(codigo_qr[0])
           
            caracteres_search =[":",","]

            posiciones =[]

            for i in range(len(dataqr)):
                if dataqr[i] in caracteres_search:
                    posiciones.append(i)

            print("Los caracteres buscados se encuentran en las posiciones:")
            for posicion in posiciones:
                print(posicion)

            #Valores para crear el rango y separar el string
            var1, var2, var3, var4, var5, var6, var7, var8, var9 = posiciones

            print("Variable", var1)


            identificacion = dataqr[(var1+2):(var2)]
            print("Identificacion",identificacion)

            nombre = dataqr[(var3+2):(var4)]
            print("Nombre",nombre)

            telefono = dataqr[(var5+2):(var6)]
            print("Telefono",telefono)

            correo = dataqr[(var7+2):(var8)]
            print("Correo",correo)

            asistencia = dataqr[(var9+2):(len(dataqr)-1)]
            print("Asistencia",asistencia)

            # Obtener la hora actual
            hora_lectura = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Registrar el código QR y la hora de lectura en la base de datos
            registrar_lectura_qr(contenido, hora_lectura)

            pausa = True
            tiempo_pausa = 2

            print("Inicio del programa")

            while pausa:
                if tiempo_pausa <= 0:
                    pausa = False
                else:
                    print("Pausa de", tiempo_pausa, "segundos")
                    time.sleep(1)
                    tiempo_pausa -= 1

            print("Continuación después de la pausa")

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
            database="registroqr",
            user="root",
            password=""
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
