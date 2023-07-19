from datetime import datetime
import cv2
from pyzbar import pyzbar
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import time

def validarExistencia():
    
    diasem = datetime.today().weekday()
    print(diasem)

    cap = cv2.VideoCapture(0)

    while True:
        # Leer un fotograma de la cámara
        _, frame = cap.read()

        #ubicar el codigo QR
        

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
           
            #Identificar posiciones para separar cada dato del codigo QR
            caracteres_search =[":",","]

            posiciones =[]

            for i in range(len(dataqr)):
                if dataqr[i] in caracteres_search:
                    posiciones.append(i)

            #Valores para crear el rango y separar el string
            var1, var2, var3, var4, var5, var6, var7, var8, var9, var10 , var11 = posiciones


            num = dataqr[(var1+2):(var2)]
            id = dataqr[(var3+2):(var4)]
            nombres = dataqr[(var5+2):(var6)]
            pais = dataqr[(var7+2):(var8)]
            ciudad = dataqr[(var9+2):(var10)]
            ciudad_dos = dataqr[(var11+2):(len(dataqr)-1)]
            
            # Obtener la hora actual
            hora_lectura = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Mostrar el contenido del código QR en la consola
            print("Contenido del código QR:", contenido)
            print("Hora de lectura",hora_lectura)
        
        #Sacar el dia de la semana 
            diasem = datetime.today().weekday()
            print(diasem)

            if 2 == diasem:
        
                try:
                #registrar_lectura_qr(identificacion, nombre, hora_lectura)
                    conexion = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="registroqr"
                    )

                    # Crear un cursor para ejecutar consultas
                    cursor = conexion.cursor()

                    # Definir la consulta SQL para buscar un registro
                    consulta = "SELECT * FROM lecturas_qr WHERE id = %s OR dia_uno = %s"

                    # Valor para buscar en la columna especificada
                    valor1 = id
                    valor2 = hora_lectura

                    # Ejecutar la consulta con el valor proporcionado
                    cursor.execute(consulta, (valor1, valor2))
                    
                    # Obtener el resultado de la consulta
                    resultados = cursor.fetchall()
                    
                    # Verificar si se encontró un registro
                    if len(resultados) > 0:
                        print("Se encontraron registros:")
                        for resultado in resultados:
                             print(resultado)

                        if resultado[1]!= None:
                            cv2.putText(frame, 'Cliente ya registro su ingreso', (160,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2)
                            

                    else:
                        print("No se encontraron registros.")
                        cv2.putText(frame, 'Localizar codigo QR', (160,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2)
                        registrar_lectura_qr(num, id, nombres, hora_lectura)
                    
                except Error as e:
                    print("Error al conectar a la base de datos:", e)

                finally:
                    if conexion.is_connected():
                        conexion.close()
                        print("Conexión a la base de datos cerrada.")

            
                            
            else:
                print("Dia incorrecto")
            
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

           
        # Mostrar el fotograma
        cv2.imshow("Lector de código QR", frame)

        # Salir si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    
    # Liberar los recursos
    cap.release()
    cv2.destroyAllWindows()

def registrar_lectura_qr(num, id, nombres, hora_lectura):
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
            consulta = "INSERT INTO lecturas_qr (num, id, nombres, dia_uno) VALUES (%s, %s, %s, %s)"
            datos = (num, id, nombres,hora_lectura)
            cursor.execute(consulta, datos)
            conexion.commit()
            cursor.close()

    except Error as e:
        print("Error al conectar a la base de datos:", e)

    finally:
        if conexion.is_connected():
            conexion.close()
            print("Conexión a la base de datos cerrada.")

validarExistencia()
