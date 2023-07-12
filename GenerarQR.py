import qrcode
import mysql.connector

# Conectarse a la base de datos MySQL
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="registroqr"
)
cursor = cnx.cursor()

# Consulta para obtener los datos de la base de datos
query = "SELECT * FROM clientes"
cursor.execute(query)
resultados = cursor.fetchall()

# Generar códigos QR para cada registro en la base de datos
for fila in resultados:
    # Crear el contenido del código QR a partir de los datos de la fila
    contenido = f"identificacion: {fila[0]}, nombre: {fila[1]}, telefono: {fila[2]}, correo: {fila[3]}"
    
    # Crear el código QR
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(contenido)
    qr.make(fit=True)
    
    # Guardar el código QR en un archivo
    imagen = qr.make_image(fill_color="black", back_color="white")
    imagen.save(f"qr_{fila[0]}.png")

# Cerrar la conexión a la base de datos
cursor.close()
cnx.close()
