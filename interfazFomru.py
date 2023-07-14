import tkinter as tk
import qrcode

def generar_codigo_qr():
    # Obtener la información ingresada en el formulario
    nombre = entry_nombre.get()
    direccion = entry_direccion.get()
    telefono = entry_telefono.get()

    # Crear el contenido del código QR
    contenido_qr = f"Nombre: {nombre}\nDirección: {direccion}\nTeléfono: {telefono}"

    # Generar el código QR
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(contenido_qr)
    qr.make(fit=True)

    # Crear una imagen del código QR
    imagen_qr = qr.make_image(fill_color="black", back_color="white")
    imagen_qr.save("codigo_qr.png")

    # Mostrar una ventana con el código QR generado
    ventana_qr = tk.Toplevel()
    imagen_qr_tk = tk.PhotoImage(file="codigo_qr.png")
    label_qr = tk.Label(ventana_qr, image=imagen_qr_tk)
    label_qr.pack()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Generador de Código QR")

# Crear los elementos del formulario
label_nombre = tk.Label(ventana, text="Nombre:")
label_nombre.pack()
entry_nombre = tk.Entry(ventana)
entry_nombre.pack()

label_direccion = tk.Label(ventana, text="Dirección:")
label_direccion.pack()
entry_direccion = tk.Entry(ventana)
entry_direccion.pack()

label_telefono = tk.Label(ventana, text="Teléfono:")
label_telefono.pack()
entry_telefono = tk.Entry(ventana)
entry_telefono.pack()

boton_generar_qr = tk.Button(ventana, text="Generar Código QR", command=generar_codigo_qr)
boton_generar_qr.pack()

# Iniciar el bucle principal de la aplicación
ventana.mainloop()
