"""
Miguel Alejandro Flores Sotelo
Ángel Miguel Sanchéz Pérez
Sergio de Jesús Castillo Molano
"""

import networkx as nx
import matplotlib.pyplot as plt
import random
from collections import deque

# Parámetros
niveles = 3  # Número de niveles en el árbol

# Crear el grafo
grafo = nx.DiGraph()

# Definir el alfabeto
alfabeto = [chr(i) for i in range(97, 123)]  # Letras de la 'a' a la 'z'

# Función recursiva para construir el árbol
def crear_arbol_recursivo(grafo, nodo_padre, nivel_actual, palabra_actual=""):
    if nivel_actual <= niveles:
        letras_random = random.sample(alfabeto,len(alfabeto)) # Mezclar el alfabeto aleatoriamente
        for letra in letras_random:  # Crear nodos hijos usando el alfabeto mezclado
            nuevo_hijo = f"{palabra_actual}{letra}"  # Crear la palabra acumulada
            grafo.add_node(nuevo_hijo)  # Añadir el nuevo nodo
            grafo.add_edge(nodo_padre, nuevo_hijo)  # Conectar al nodo padre

            # Llamar recursivamente para el siguiente nivel
            crear_arbol_recursivo(grafo, nuevo_hijo, nivel_actual + 1, nuevo_hijo)

# Función para buscar una palabra en el árbol utilizando búsqueda a lo ancho como una cola
def buscar_palabra_ancho(grafo, palabra):
    # Usar una cola para la búsqueda en amplitud
    cola = deque(["raiz"])  # Iniciar la cola con el nodo raíz
    nodos_recorridos = 0  # Contador de nodos recorridos

    while len(cola) > 0:
        nodo_actual = cola.popleft()  # Sacar el nodo de la cola
        nodos_recorridos += 1  # Incrementar el contador

        # Comprobar si el nodo actual es igual a la palabra
        if nodo_actual == palabra:
            return True, nodos_recorridos  # Se encontró la palabra y el número de nodos recorridos
        # Añadir hijos a la cola
        else:
            for hijo in grafo[nodo_actual]:
                cola.append(hijo)  # Añadir los hijos a la cola
    return False, nodos_recorridos  # La palabra no se encontró

# Función para buscar una palabra en el árbol utilizando búsqueda a lo profundo como una pila
def buscar_palabra_profundo(grafo, palabra):
    # Usar una pila para la búsqueda en profundidad
    pila = deque(["raiz"])  # Iniciar la pila con el nodo raíz
    nodos_recorridos = 0  # Contador de nodos recorridos (inicia desde 1 porque 0 es la raiz)
    partes_muñeco = 0  # Contador de partes del muñeco dibujadas
    nodos_por_error = 4  # Nodos por error

    while len(pila) > 0:
        nodo_actual = pila.pop()  # Sacar el nodo de la pila
        nodos_recorridos += 1  # Incrementar el contador

        # Comprobar si el nodo actual es igual a la palabra
        if nodo_actual == palabra:
            return True, nodos_recorridos  # Se encontró la palabra y el número de nodos recorridos
        # Añadir hijos a la pila
        else:
            for hijo in reversed(list(grafo[nodo_actual])):
                pila.append(hijo)  # Añadir los hijos a la pila
            
            # Si se han recorrido 3 nodos sin encontrar la palabra, incrementar partes del muñeco
            if nodos_recorridos % nodos_por_error == 0:
                partes_muñeco += 1
                dibujar_muñeco(partes_muñeco)

            # Si se han dibujado todas las partes del muñeco, terminar el juego
            if partes_muñeco == 6:
                print("El muñeco está completo. Has perdido.")
                return False, nodos_recorridos
    return False, nodos_recorridos  # La palabra no se encontró

def dibujar_muñeco(partes_muñeco):
    # Crear el canvas de dibujo
    fig, ax = plt.subplots()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Dibujar la base de la horca
    ax.plot([1, 5], [1, 1], color='black', lw=2)  # Base
    ax.plot([3, 3], [1, 8], color='black', lw=2)  # Poste
    ax.plot([3, 6], [8, 8], color='black', lw=2)  # Soporte superior
    ax.plot([6, 6], [8, 7], color='black', lw=2)  # Cuerda

    # Dibujar partes del muñeco según el número de errores
    if partes_muñeco > 0:
        ax.plot([6], [6.5], 'o', color='black', markersize=15)  # Cabeza
    if partes_muñeco > 1:
        ax.plot([6, 6], [6, 5], color='black', lw=2)  # Cuerpo
    if partes_muñeco > 2:
        ax.plot([6, 5.5], [5.5, 5], color='black', lw=2)  # Brazo izquierdo
    if partes_muñeco > 3:
        ax.plot([6, 6.5], [5.5, 5], color='black', lw=2)  # Brazo derecho
    if partes_muñeco > 4:
        ax.plot([6, 5.5], [4.5, 4], color='black', lw=2)  # Pierna izquierda
    if partes_muñeco > 5:
        ax.plot([6, 6.5], [4.5, 4], color='black', lw=2)  # Pierna derecha

    plt.title(f"Intentos fallidos: {partes_muñeco}")
    plt.show()





# Llamar a la función para crear el árbol desde la raíz
crear_arbol_recursivo(grafo, "raiz", 1)
palabra_a_buscar = "aab"  # Palabra de búsqueda


encontrada_a_lo_ancho, nodos_a_lo_ancho = buscar_palabra_ancho(grafo, palabra_a_buscar)
encontrada_a_lo_profundo, nodos_a_lo_profundo = buscar_palabra_profundo(grafo, palabra_a_buscar)

print("BUSQUEDA A LO ANCHO")
if encontrada_a_lo_ancho:
    print(f"La palabra '{palabra_a_buscar}' fue encontrada en el árbol a lo ancho. Nodos recorridos: {nodos_a_lo_ancho}")
else:
    print(f"La palabra '{palabra_a_buscar}' no fue encontrada en el árbol a lo ancho. Nodos recorridos: {nodos_a_lo_ancho}")

print("\n")

print("BUSQUEDA A LO PROFUNDO")
if encontrada_a_lo_profundo:
    print(f"La palabra '{palabra_a_buscar}' fue encontrada en el árbol a lo profundo. Nodos recorridos: {nodos_a_lo_profundo}")
else:
    print(f"La palabra '{palabra_a_buscar}' no fue encontrada en el árbol a lo profundo. Nodos recorridos: {nodos_a_lo_profundo}")

