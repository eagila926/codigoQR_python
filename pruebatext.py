dataqr= ("b'identificacion: 27-857-5550, nombre: Tempsoft, telefono: 1924176914, correo: kscuddersdv@syman.com, asistencia: 0'")
print(len(dataqr))        
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


