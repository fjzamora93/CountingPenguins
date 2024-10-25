"""
CREAR EL SIGUIENTE CÓDIGO:

-Iterar sobre las imágenes de la ruta 'tiles_coords/tiles' 
-Para cada imagen, obtener el nombre del archivo sin la extensión
-Comprobar si el archivo con el mismo nombre pero .txt de la carpeta 'tiles_coords/labels' está vacío.
-Si el archivo NO está vacío, copiar la imagen a la carpeta 'data/images/train' y el txt a 'data/labels/train'

"""
# VAMOS A SEPARAR MANUALMENTE LOS DATOS DE ENTRENAMIENTO Y PRUEBA, CONCRETAMENTE VAMOS A SEPARAR 70-30
#  105 PARA TRAIN Y 44 PARA VAL

import os 
import shutil

IMGS_PATH = os.path.join('tiles_coords', 'subtiles')

for img in os.listdir(IMGS_PATH):
    try:
        img_name = os.path.splitext(img)[0]
        txt_path = os.path.join('tiles_coords', 'labels', f'{img_name}.txt')
        if os.path.getsize(txt_path) > 0:
            img_full_path = os.path.join(IMGS_PATH, img)
            txt_full_path = os.path.join('tiles_coords', 'labels', f'{img_name}.txt')

            shutil.copy(img_full_path, os.path.join('data', 'images', 'train'))
            shutil.copy(txt_full_path, os.path.join('data', 'labels', 'train'))
            print(f"Imagen {img} y archivo {txt_path} copiados a 'data/images/train' y 'data/labels/train' respectivamente.")
        else:
            print(f"Archivo {txt_path} vacío. No se copiará la imagen {img}.")
    except FileNotFoundError as e:
        print(f"Archivo {txt_path} no encontrado. No se copiará la imagen {img}.Error: {e}")