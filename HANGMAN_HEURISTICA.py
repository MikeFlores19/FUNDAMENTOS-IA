"""
Miguel Alejandro Flores Sotelo
Juan Carlos Flores Mora
Sergio de Jesús Castillo Molano
"""
import networkx as nx
import heapq
import random

#Numero de niveles del arbol
niveles=5

#Crear el grafo
grafo=nx.DiGraph()

#Definir el alfabeto
alfabeto=[chr(i) for i in range(97,123)] #Letras de la 'a' a la 'z'

def crear_arbol_recursivo(grafo,nodo_padre,nivel_actual,palabra_actual=""):
    if nivel_actual<=niveles:
        if nivel_actual == 1:
            letras_random=random.sample(alfabeto,len(alfabeto)) #Mezclar el alfabeto aleatoriamente
        else:
            vocales = "aeiou"
            letras = ""
            #Se obtiene la última letra, esto para verificar qué letra es y no generar de nuevo las 27 letras
            ultima_letra = nodo_padre[-1]
            #Combinaciones con vocales
            if ultima_letra in vocales:
                letras = random.sample(alfabeto,len(alfabeto))
            else:
                #Combinaciones dependiendo de la consonante
                if ultima_letra == "l":
                    letras = "l" + vocales
                elif ultima_letra in "drt":
                    letras = "r" + vocales
                elif ultima_letra in "bcfghkp":
                    letras = "lr" + vocales
                    if ultima_letra == "c":
                        letras = "c" + letras
                    if ultima_letra == "p":
                        letras = "s" + letras 
                else:
                    letras = vocales
            letras_random = random.sample(letras,len(letras))
        for letra in letras_random: #Crear nodos hijos usando el alfabeto mezclado
            nuevo_hijo= f"{palabra_actual}{letra}" #Crear la palabra acumulada
            grafo.add_node(nuevo_hijo) #Añadir el nuevo hijo
            grafo.add_edge(nodo_padre,nuevo_hijo)#Conecta el nodo padre con el nodo hijo

            crear_arbol_recursivo(grafo,nuevo_hijo,nivel_actual + 1, nuevo_hijo)

#FUNCION HEURISITCA MIDE CUAN CERCA ESTA UNA PALABRA DE UN OBJETIVO
def heuristica(palabra_actual,palabra_objetivo):
    coincidencias=0
    for i in range(min(len(palabra_actual),len(palabra_objetivo))):#Compara los caracteres en un rango de la palabra mas corta para que no haya errores
        if (palabra_actual[i]==palabra_objetivo[i]):
            coincidencias+=1
        else:
            break #Dejar de contar los caracteres que ya no coinciden
    return -coincidencias # Se usa negativo porque 'heapq' (modulo o cola de prioridad) prioriza los valores mas pequeños

#BUSQUEDA HEURISTICA CON COLA DE PRIORIDAD (GREEDY BEST-FIRST SEARCH)
def busqueda_heuristica(grafo,palabra_objetivo):
    cola_prioridad=[] #Usar una cola de prioridad basada en la heuristica
    heapq.heappush(cola_prioridad,(heuristica("raiz",palabra_objetivo),"raiz"))#Iniciar con la raiz

    #Ciclo de busqueda
    nodos_recorridos=0 #Variable de conteo para los nodos recorridos
    visitados= set() #Conjunto vacio (similar a una lista pero no permite duplicados y permite busquedas rapidas)

    while (len(cola_prioridad)>0):
        _, nodo_actual= heapq.heappop(cola_prioridad) #Desempaca el nodo con menor heuristica (mayor coincidencia), el _ es para indicar que la heuristica no importa, entonces solo saca la palabra (nodo)
        nodos_recorridos+=1 #Aumentamos el numero de nodos recorridos
    
        #Comprobar si encontramos la palabra
        if (nodo_actual== palabra_objetivo):
            return True, nodos_recorridos #Se encontro la palabra
        
        #Si el nodo no ha sido visitado antes
        if (nodo_actual) not in visitados:
            visitados.add(nodo_actual)

            #Añadir los hijos a la cola de prioridad con su respectiva heuristica
            for hijo in grafo[nodo_actual]: #Por cada hijo del nodo actual (nodos conectados al nodo actual), calculamos su heuristica con respecto a la palabra objetivo
                if (hijo not in visitados):
                    heapq.heappush(cola_prioridad,(heuristica(hijo,palabra_objetivo),hijo)) #Añadimos estos hijos a la cola de prioridad para que sean procesados mas tarde
    
    return False, nodos_recorridos #Si no se encontro la palabra



#Crear el arbol desde la raíz
crear_arbol_recursivo(grafo,"raiz",1)
print("ARBOL CREADO\n")

#Palabra a buscar
palabra_a_buscar="cazerola"

encontrada,nodos= busqueda_heuristica(grafo,palabra_a_buscar)

#Resultadso
print("BUSQUEDA HEURISTICA\n")

if (encontrada==1):
    print(f"La palabra '{palabra_a_buscar}' fue encontrada en el árbol con la búsqueda heurística (GREEDY BEST-FIRST SEARCH). Nodos recorridos: {nodos}")

else:
    print(f"La palabra '{palabra_a_buscar}' no fue encontrada en el árbol con la búsqueda heurística (GREEDY BEST-FIRST SEARCH). Nodos recorridos: {nodos}")






