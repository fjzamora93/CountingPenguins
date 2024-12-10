import utils.yolo_fun as yolo_fun
import utils.img_fun as img_fun
import os
import pandas as pd
from tqdm import tqdm  
import rasterio
from rasterio.windows import Window
from rasterio.errors import RasterioIOError
import numpy as np
import shutil

#valid_tiles = [13, 14, 15, 22, 23, 24, 52, 53, 61, 62, 63, 72, 81, 82]  

orthomosiac_coords = os.path.join('coords', 'yolo_coords.csv')
coords_dir_sin_normalizar = os.path.join('coords', 'labels_sin_normalizar')
coords_dir_normalized = os.path.join('coords', 'labels_normalized')
os.makedirs(coords_dir_sin_normalizar, exist_ok=True)
os.makedirs(coords_dir_normalized, exist_ok=True)

# PARTE 0: ITERAMOS SOBRE LAS IMÁGENES PARA RECORTARLAS


for n_tile in range(14, 99):
    try:
        # PARTE 1: Cargar la imagen y recortarla en imágenes más pequeñas de aproximadamente 500x500 píxeles
        print(f"\n\nRecortando imagen {n_tile}...")
        print('_________________________________________________________')
        NUM_TILE = n_tile
        path_doctorado = 'G:\\.shortcut-targets-by-id\\1pYgV5EIk4-LapLNhlCwpQaDAzuqNffXG\\doctorado_albert\\conteo_pinguinos'
        subrecortes_dir = os.path.join('cut_tiles')
        os.makedirs(subrecortes_dir, exist_ok=True)

        image_name = f"recortes/recorte_{NUM_TILE}.tif"
        tiff_file = os.path.join(path_doctorado, image_name)


        # Sacamos un diccionario con toda la información de la imagen
        img_info = img_fun.get_img_info(tiff_file)
        WIDTH = img_info["width"]
        HEIGHT = img_info["height"]
        TOP_LEFT = img_info["top_left"]
        BOTTOM_RIGHT = img_info["bottom_right"]
        min_x, max_y = img_info['top_left']
        max_x, min_y = img_info['bottom_right']

        img_fun.crop_tile_into_subrecortes(tiff_file, subrecortes_dir, NUM_TILE)


        # PARTE 2 (OPCIONAL): EXTRACCIÓN DE METADATOS PARA CADA SUBRECORTE INDIVIUAL
        df_orthomosaic = pd.read_csv(orthomosiac_coords, encoding='ISO-8859-1')
        print("Datos Originales: \n", df_orthomosaic.head())

        # Filtrar los puntos que están dentro del tile
        filtered_data = df_orthomosaic[
            (df_orthomosaic['x_center'] >= min_x) & (df_orthomosaic['x_center'] <= max_x) &
            (df_orthomosaic['y_center'] >= min_y) & (df_orthomosaic['y_center'] <= max_y)
        ]
        filtered_data.to_csv(os.path.join('coords', 'coords_per_tile' ,f'coords_{NUM_TILE}.csv'), index=False)
        print(f"Datos filtrados guardados en 'coords/coords_per_tile/coords_{NUM_TILE}.csv'.")

        # PARTE 3: ASIGNACIÓN DE LABELS EN TXT A CADA SUBRECORTE
        yolo_fun.generar_txt_yolo(subrecorte_dir=subrecortes_dir)
    except RasterioIOError as e:
        print(f"Error al cargar la imagen con rasterio: {e}")
        continue
    except FileNotFoundError as e:
        print(f"Error: {e}")
        continue
    except Exception as e:
        print(f"Error: {e}")
        continue
    


# Iteramos para normalizar las coordenadas de cara archivo.txt
for file in os.listdir(coords_dir_sin_normalizar):
    df_sin_normalizar = pd.read_csv(os.path.join(coords_dir_sin_normalizar, file), sep=' ', header=None)
    name_subrecorte = os.path.splitext(file)[0]
    subrecorte_file = os.path.join('cut_tiles', f"{name_subrecorte}.tiff")

    print(f"Normalizando archivo {file}...")
    coords_file = os.path.join(coords_dir_sin_normalizar, file)
    output_file = os.path.join(coords_dir_normalized, file)
    
    yolo_fun.normalize_yolo_coords(
        tiff_file = subrecorte_file,
        coords_sin_normalizar = df_sin_normalizar, 
        output_file = output_file, 
    )


# PARTE 4: CLASIFICAR CONJUNTOS DE TRAIN Y VAL
for n_tile in range(14, 99):
    try:
        counter = 0
        subrecorte_dir = os.path.join('cut_tiles')
        for img in os.listdir(subrecorte_dir):
          
            img_name = os.path.splitext(img)[0]  # Divide entre el nombre del archivo y la extensión
            txt_path = os.path.join(coords_dir_normalized, f'{img_name}.txt')
            
            if os.path.getsize(txt_path) > 0:  # Solo copiar si el archivo .txt tiene contenido
                img_full_path = os.path.join(subrecorte_dir, img)
                txt_full_path = os.path.join(coords_dir_normalized, f'{img_name}.txt')

                # Alternar entre train y val con el contador
                if counter >= 9:
                    shutil.copy(img_full_path, os.path.join('datasets', 'penguin_dataset', 'images', 'val'))
                    shutil.copy(txt_full_path, os.path.join('datasets', 'penguin_dataset', 'labels', 'val'))
                    print(f"Imagen {img} y archivo {txt_path} copiados a 'datasets/penguin_dataset/images/val' y 'datasets/penguin_dataset/labels/val'.")
                else:
                    shutil.copy(img_full_path, os.path.join('datasets', 'penguin_dataset', 'images', 'train'))
                    shutil.copy(txt_full_path, os.path.join('datasets', 'penguin_dataset', 'labels', 'train'))
                    print(f"Imagen {img} y archivo {txt_path} copiados a 'datasets/penguin_dataset/images/train' y 'datasets/penguin_dataset/labels/train'.")
                
                counter = 0 if counter >= 10 else counter + 1
            
            else:
                print(f"Archivo {txt_path} vacío. No se copiará la imagen {img}.")
  
    except FileNotFoundError as e:
        print(f"Error: {e}")
        continue
    except Exception as e:
        print(f"Error: {e}")
        continue