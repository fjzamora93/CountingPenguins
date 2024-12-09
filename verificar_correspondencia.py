import os

def verificar_y_eliminar_sin_correspondencia(img_dir, label_dir):
    # Obtener la lista de archivos en el directorio de imágenes
    img_files = os.listdir(img_dir)
    # Obtener la lista de archivos en el directorio de etiquetas
    label_files = os.listdir(label_dir)
    
    # Crear conjuntos de nombres base de archivos sin extensiones
    img_names = {os.path.splitext(img_file)[0] for img_file in img_files}
    label_names = {os.path.splitext(label_file)[0] for label_file in label_files}
    
    # Encontrar archivos de imagen sin correspondencia
    img_without_labels = img_names - label_names
    # Encontrar archivos de etiqueta sin correspondencia
    labels_without_img = label_names - img_names
    
    # Eliminar archivos de imagen sin correspondencia
    for img_name in img_without_labels:
        img_full_path = os.path.join(img_dir, f'{img_name}.jpg')  # Asumiendo que las imágenes son .jpg
        if os.path.exists(img_full_path):
            os.remove(img_full_path)
            print(f"Archivo de imagen {img_full_path} eliminado porque no tiene un archivo .txt correspondiente.")
    
    # Eliminar archivos de etiqueta sin correspondencia
    for label_name in labels_without_img:
        label_full_path = os.path.join(label_dir, f'{label_name}.txt')
        if os.path.exists(label_full_path):
            os.remove(label_full_path)
            print(f"Archivo de etiqueta {label_full_path} eliminado porque no tiene un archivo de imagen correspondiente.")

# Directorios de imágenes y etiquetas usando rutas relativas
img_dir = os.path.join('.', 'datasets', 'penguin_dataset', 'images', 'train')
label_dir = os.path.join('.', 'datasets', 'penguin_dataset', 'labels', 'train')

# Llamar a la función para verificar y eliminar archivos sin correspondencia
verificar_y_eliminar_sin_correspondencia(img_dir, label_dir)