import os
import cv2
import numpy as np
import pandas as pd
from skimage.feature import hog
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import seaborn as sns

# ETAPA 1 : CARGAR Y PREPROCESAR DATOS
data_direccion = "monedas"
clases = ["un_peso", "dos_pesos", "cinco_pesos"]

X = []  # Características
Y = []  # Etiquetas

# Leer las imágenes y extraer características con HOG (Histograma de gradientes orientado)
for etiqueta, clase_moneda in enumerate(clases):
    folder = os.path.join(data_direccion, clase_moneda)
    for nombre_archivo in os.listdir(folder):
        ruta_imagen = os.path.join(folder, nombre_archivo)
        imagen = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
        if imagen is not None:
            # Redimensionar la imagen correctamente
            imagen = cv2.resize(imagen, (64, 64))
            # Extraer características HOG
            caracteristicas, visualizacion = hog(imagen, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=True)
            X.append(caracteristicas)
            Y.append(etiqueta)

X = np.array(X)
Y = np.array(Y)

# Dividir los datos en entrenamiento y prueba
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# Aplicar PCA para reducir a 2 dimensiones
pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train)
X_test_pca = pca.transform(X_test)

# Crear un gráfico para los datos de entrenamiento
plt.figure(figsize=(10, 8))
colores = ['blue', 'green', 'red']
for etiqueta, nombre_clase, color in zip(np.unique(Y_train), clases, colores):
    indices = np.where(Y_train == etiqueta)
    plt.scatter(X_train_pca[indices, 0], X_train_pca[indices, 1], label=nombre_clase, color=color, alpha=0.7)
plt.xlabel("Componente Principal 1")
plt.ylabel("Componente Principal 2")
plt.title("Distribución de datos con PCA (Entrenamiento)")
plt.legend()
plt.grid()
plt.show()

# Crear un gráfico para los datos de prueba
plt.figure(figsize=(10, 8))
for etiqueta, nombre_clase, color in zip(np.unique(Y_test), clases, colores):
    indices = np.where(Y_test == etiqueta)
    plt.scatter(X_test_pca[indices, 0], X_test_pca[indices, 1], label=nombre_clase, color=color, alpha=0.7)
plt.xlabel("Componente Principal 1")
plt.ylabel("Componente Principal 2")
plt.title("Distribución de datos con PCA (Prueba)")
plt.legend()
plt.grid()
plt.show()

# AGREGAR MATRIZ DE CORRELACIÓN ANTES DE LA ETAPA 2
# Crear un DataFrame con los datos procesados por PCA
pca_features_train = pd.DataFrame(X_train_pca, columns=['PCA1', 'PCA2'])
pca_features_train['Etiqueta'] = Y_train

# Calcular la matriz de correlación
correlation_matrix = pca_features_train.corr()

# Graficar la matriz de correlación
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Matriz de correlación (después de PCA)")
plt.show()

# ETAPA 2 : ENTRENAR EL MODELO RANDOM FOREST
modelo_knn = KNeighborsClassifier(n_neighbors=3)
modelo_knn.fit(X_train, Y_train)

# Crear un gráfico para los datos clasificados por KNN (Entrenamiento)
Y_train_pred = modelo_knn.predict(X_train)
plt.figure(figsize=(10, 8))
for etiqueta, nombre_clase, color in zip(np.unique(Y_train_pred), clases, colores):
    indices = np.where(Y_train_pred == etiqueta)
    plt.scatter(X_train_pca[indices, 0], X_train_pca[indices, 1], label=f"{nombre_clase} (Clasificado)", color=color, alpha=0.7, edgecolor='k')
plt.xlabel("Componente Principal 1")
plt.ylabel("Componente Principal 2")
plt.title("Clasificación de datos con KNN (Entrenamiento)")
plt.legend()
plt.grid()
plt.show()

# ETAPA 3: EVALUAR EL MODELO
Y_pred = modelo_knn.predict(X_test)
accuracy = accuracy_score(Y_test, Y_pred)
print(f"Precisión del modelo KNN: {accuracy * 100:.2f}%")

# Gráfica para los datos clasificados por KNN (Prueba)
plt.figure(figsize=(10, 8))
for etiqueta, nombre_clase, color in zip(np.unique(Y_pred), clases, colores):
    indices = np.where(Y_pred == etiqueta)
    plt.scatter(X_test_pca[indices, 0], X_test_pca[indices, 1], label=f"{nombre_clase} (Clasificado)", color=color, alpha=0.7, edgecolor='k')
plt.xlabel("Componente Principal 1")
plt.ylabel("Componente Principal 2")
plt.title("Clasificación de datos con KNN (Prueba)")
plt.legend()
plt.grid()
plt.show()

# Mostrar la matriz de confusión
conf_matrix = confusion_matrix(Y_test, Y_pred)

# Graficar la matriz de confusión
plt.figure(figsize=(6, 5))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap="Blues", xticklabels=clases, yticklabels=clases)
plt.xlabel("Predicción")
plt.ylabel("Real")
plt.title("Matriz de Confusión")
plt.show()

# Mostrar el reporte de clasificación (accuracy, precision, f1 score, support)
report = classification_report(Y_test, Y_pred, target_names=clases)
print("\nReporte de Clasificación:")
print(report)



# ETAPA 4 : CLASIFICACION IMAGEN
def clasificar_imagen_cargada(ruta_imagen):
    etiqueta_a_moneda = {0: "1 Peso", 1: "2 pesos", 2: "5 pesos"}
    
    # Leer la imagen original
    imagen_original = cv2.imread(ruta_imagen)
    if imagen_original is None:
        print("Error: No se pudo cargar la imagen.")
        return

    # Convertir a escala de grises y redimensionar
    gris = cv2.cvtColor(imagen_original, cv2.COLOR_BGR2GRAY)
    imagen = cv2.resize(gris, (64, 64))

    # Extraer características HOG
    caracteristicas, _ = hog(imagen, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=True)
    caracteristicas = np.array(caracteristicas).reshape(1, -1)

    # Predecir la clase
    prediccion = modelo_knn.predict(caracteristicas)[0]
    nombre_moneda = etiqueta_a_moneda[prediccion]

    # Mostrar el resultado
    print(f"La imagen clasificada es: {nombre_moneda}")

    # Ajustar la imagen a la ventana
    height, width = imagen_original.shape[:2]
    max_height, max_width = 800, 800  # Tamaño máximo de la ventana
    scaling_factor = min(max_width / width, max_height / height)
    nueva_dim = (int(width * scaling_factor), int(height * scaling_factor))
    imagen_redimensionada = cv2.resize(imagen_original, nueva_dim)

    # Mostrar la imagen original con la predicción superpuesta
    cv2.putText(imagen_redimensionada, nombre_moneda, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Clasificación de Moneda", imagen_redimensionada)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Ejemplo de uso
clasificar_imagen_cargada("prueba_monedas/5.2.jpg")  # Reemplaza con la ruta de tu imagen
