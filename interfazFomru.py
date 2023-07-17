import tkinter as tk
import qrcode
import cv2
from pyzbar import pyzbar
import mysql.connector
from mysql.connector import Error
from datetime import datetime
import time

def generar_codigo_qr():
    # Obtener la información ingresada en el formulario
    identificacion = entry_identificacion.get()
    nombre = entry_nombre.get()
    direccion = entry_correo.get()
    telefono = entry_telefono.get()

    # Crear el contenido del código QR
    contenido_qr = f"Identificacion: {identificacion}, Nombre: {nombre}, Telefono: {telefono}, Correo: {direccion}"

    # Generar el código QR
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(contenido_qr)
    qr.make(fit=True)

    # Crear una imagen del código QR
    imagen_qr = qr.make_image(fill_color="black", back_color="white")
    imagen_qr.save("qr_"+identificacion+".png")

    # Mostrar una ventana con el código QR generado
    ventana_qr = tk.Toplevel()
    imagen_qr_tk = tk.PhotoImage(file="qr_"+identificacion+".png")
    label_qr = tk.Label(ventana_qr, image=imagen_qr_tk)
    label_qr.pack()

    
def registrar_lectura_qr(identificacion, nombre, hora_lectura):
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
            consulta = "INSERT INTO lecturas_qr (contenido, nombre, dia_uno) VALUES (%s, %s, %s)"
            datos = (identificacion, nombre, hora_lectura)
            cursor.execute(consulta, datos)
            conexion.commit()
            cursor.close()

    except Error as e:
        print("Error al conectar a la base de datos:", e)

    finally:
        if conexion.is_connected():
            conexion.close()
            print("Conexión a la base de datos cerrada.")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Generador de Código QR")

# Crear los elementos del formulario
label_identificacion = tk.Label(ventana, text="Identificacion:")
label_identificacion.pack()
entry_identificacion = tk.Entry(ventana)
entry_identificacion.pack()

label_nombre = tk.Label(ventana, text="Nombre: ")
label_nombre.pack()
entry_nombre = tk.Entry(ventana)
entry_nombre.pack()

label_telefono = tk.Label(ventana, text="Telefono: ")
label_telefono.pack()
entry_telefono = tk.Entry(ventana)
entry_telefono.pack()

label_correo = tk.Label(ventana, text="Correo: ")
label_correo.pack()
entry_correo = tk.Entry(ventana)
entry_correo.pack()



boton_generar_qr = tk.Button(ventana, text="Generar Código QR", command=generar_codigo_qr)
boton_generar_qr.pack()

# Iniciar el bucle principal de la aplicación
ventana.mainloop()
