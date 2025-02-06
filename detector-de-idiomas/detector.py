import os

textos_procesados = []

try:
    with open("textos\\textos_registrados.txt", encoding="UTF-8") as archivo_aprendido:
        procesado = archivo_aprendido.read()
        textos_procesados = procesado.split(";")
        textos_procesados.pop()
except FileNotFoundError:
    pass

def lectura_registro(idioma_registro):
    #Diccionario que almacena la frecuencia de cada letra
    diccionario_letras = {}

    #Abrimos el registro para acumular las frecuencias conforme le damos más textos en el idioma en cuestión
    try:
        with open(idioma_registro, encoding="UTF-8") as registro_input:
            for linea in registro_input.readlines():
                letra, frecuencia = linea.split(": ")
                diccionario_letras[letra] = int(frecuencia)
    except FileNotFoundError:
        pass
    return diccionario_letras

def escritura_registro(diccionario, idioma_registro):
    #Guarda los valores finales actualizados en el mismo archivo de registro
    with open (idioma_registro, 'w',encoding="UTF-8") as registro:
        for llave, valor in diccionario.items():
            registro.write(f"{llave}: {valor}\n")

def conteo_letras(diccionario, texto_por_procesar):
    #Realiza el conteo de las letras
    encontrado = 1
    try:
        with open (texto_por_procesar, encoding= "UTF-8") as archivo:
            for linea in archivo.readlines():
                #print(linea)
                linea = linea.upper()
                for letra in linea:
                    if letra.isalpha():
                        try:
                            diccionario[letra] += 1
                        except KeyError:
                            diccionario[letra] = 1
    except FileNotFoundError:
        print("Este archivo no existe.")
        encontrado = 0
    return diccionario, encontrado

def registro_leidos(procesados):
    with open("textos\\textos_registrados.txt", 'w',encoding="UTF-8") as archivo_aprendido:
        for nombre in procesados:
            archivo_aprendido.write(f"{nombre};")

def frecuencia_relativa(diccionario):
    total_palabras = 0
    f_r = {} #nuevo diccionario de frecuencias relativas para cada letra
    for llave, valor in diccionario.items():
        total_palabras += valor #se va sumando el valor de cada letra (a,b,c,d...) para obtener el total de letras
        
    for llave, valor in diccionario.items():
        f_r[llave] = valor / total_palabras #se obtiene la frecuencia relativa de cada letra
        
    return f_r, total_palabras #devuelve el el diccionario de letra:frecuencia relativa y el total de letras registradas

def calculo_probabilidad(fre_texto, fre_rel_idioma, total_idioma):
    probabilidad = 1
    for llave, valor in fre_texto.items():
        try:
            probabilidad *= fre_rel_idioma[llave] * valor
        except KeyError:
            #Suavizado de Laplace se usa para manejar elementos (letras) que no esten presente en el idioma de fre_realitva_idioma 
            fre_relativa = 1 / (total_idioma + 50) #parametro  de suavizado es el 50
            probabilidad *= fre_relativa * valor
    
    return probabilidad

def suma_frecuencias(fre_texto, fre_idioma):
    for llave, valor in fre_texto.items():
        try:
            fre_idioma[llave] += valor
        except KeyError:
            fre_idioma[llave] = valor
            
    return fre_idioma

while True:
    print("-------------------------------------------")
    print("Bienvenido al menú. ¿Qué deseas hacer?")
    print("\t[1] Entrenar agente.")
    print("\t[2] Clasificar texto.")
    print("\t[0] Salir.")
    print("-------------------------------------------")
    opcion = int(input("Ingresa una opción: "))

    os.system("cls")
    
    if opcion == 1:
        #aquí va la parte de entrenamiento
        #Verifica que el archivo a procesar no haya sido utilizado anteriormente
        nombre_archivo = input("Introduce el nombre del archivo a procesar: ")
        while nombre_archivo in textos_procesados:
            nombre_archivo = input("Este texto ya fue procesado. Por favor, ingresa otro: ")
        

        idioma_archivo = input("Ingresa el idioma en que está el archivo: ")
        idioma_archivo = idioma_archivo.lower()

        #Para almacenar en el registro de entrenamiento
        if idioma_archivo == "español":
            idioma_archivo = "espaniol"
        elif idioma_archivo == "inglés" or idioma_archivo == "ingles":
            idioma_archivo = "ingles"
        elif idioma_archivo == "francés" or idioma_archivo == "francés":
            idioma_archivo = "frances"
        else:
            print("Error, idioma no manejado.")
            continue
        
        #Creación de las rutas
        ruta_archivo = "textos\\" + idioma_archivo + "\\" + nombre_archivo 
        ruta_registro = "textos\\" + idioma_archivo + "\\" + idioma_archivo + ".txt"
        
        #Se guarda en un diccionario la frecuencia registrada en el archivo
        registro = lectura_registro(ruta_registro)
        
        #Se hace el conteo de las letras
        registro, found = conteo_letras(registro, ruta_archivo)
        
        #Guarda las frecuencias actualizadas
        escritura_registro(registro, ruta_registro)
        
        if found == 1:
            #Agrega el texto procesado al registro de los que ya fueron leídos
            textos_procesados.append(nombre_archivo)
            registro_leidos(textos_procesados)

    elif opcion == 2:
        #Aquí va la clasificación
        
        #Verifica que el archivo a procesar no haya sido utilizado anteriormente
        nombre_archivo = input("Introduce el nombre del archivo a procesar: ")
        while nombre_archivo in textos_procesados:
            nombre_archivo = input("Este texto ya fue procesado. Por favor, ingresa otro: ")
        
        
        #Creación de las rutas
        ruta_archivo = "textos\\pruebas\\" + nombre_archivo 
        ruta_espaniol = "textos\\espaniol\\espaniol.txt" 
        ruta_frances = "textos\\frances\\frances.txt"
        ruta_ingles = "textos\\ingles\\ingles.txt"
        
        #Se guarda en un diccionario las frecuencias registradas en el idioma
        frecuencia_esp = lectura_registro(ruta_espaniol)
        frecuencia_ing = lectura_registro(ruta_ingles)
        frecuencia_fra = lectura_registro(ruta_frances)
        
        #Se calcula la frecuencia relativa y el total de las letras de cada idioma
        fre_rel_esp, total_esp = frecuencia_relativa(frecuencia_esp)
        fre_rel_ing, total_ing = frecuencia_relativa(frecuencia_ing)
        fre_rel_fra, total_fra = frecuencia_relativa(frecuencia_fra)
        
        #Frecuencia del archivo a clasificar
        frecuencia_texto, found = conteo_letras({}, ruta_archivo)
        
        if found == 1:
            #Calculo de las probabilidades de que pertenezca a ese idioma
            prob_esp = calculo_probabilidad(frecuencia_texto, fre_rel_esp, total_esp)
            prob_ing = calculo_probabilidad(frecuencia_texto, fre_rel_ing, total_ing)
            prob_fra = calculo_probabilidad(frecuencia_texto, fre_rel_fra, total_fra)

            #Impresión de probabilidades
            print()
            print("---------------------------------------------")
            print(f"Probabilidad de español: {prob_esp:.10f}")
            print(f"Probabilidad de inglés: {prob_ing:.10f}" )
            print(f"Probabilidad de francés: {prob_fra:.10f}")
            print("---------------------------------------------")
            print()
            
            #Suma las frecuencias del texto con el del idioma detectado
            if prob_esp > prob_fra and prob_esp > prob_ing:
                print("Este archivo está en idioma español.")
                frecuencia_esp = suma_frecuencias(frecuencia_texto, frecuencia_esp)
                escritura_registro(frecuencia_esp, ruta_espaniol)
            if prob_ing > prob_esp and prob_ing > prob_fra:
                print("Este archivo está en idioma inglés.")
                frecuencia_ing = suma_frecuencias(frecuencia_texto, frecuencia_ing)
                escritura_registro(frecuencia_ing, ruta_ingles)
            if prob_fra > prob_esp and prob_fra > prob_ing:
                print("Este archivo está en idioma francés.")
                frecuencia_fra = suma_frecuencias(frecuencia_texto, frecuencia_fra)
                escritura_registro(frecuencia_fra, ruta_frances)
            print()
            #Agrega el texto procesado al registro de los que ya fueron leídos
            textos_procesados.append(nombre_archivo)
            registro_leidos(textos_procesados) 
    elif opcion == 0:
        print("¡Hasta la vista!")
        break
    else:
        print("Esa opción no existe, por favor, intenta con una válida.")