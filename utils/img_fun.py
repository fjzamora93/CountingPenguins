
import os
import pandas as pd
from tqdm import tqdm  
import rasterio
from typing import Tuple
from rasterio.windows import Window
import numpy as np

# Funciones para el procesamiento de imágenes
def hello():
    print("Hello, world!")



def get_img_info(img_path: str) -> dict:
    """
    Abre una imagen con rasteiro y devuelve un diccionario con toda la información clave sobre la imagen.

    Args:
    - full_image_path: el path completo de la imagen.
    """
    img_dict = {}

    with rasterio.open(img_path) as src:
        transform = src.transform  # Transformación de coordenadas (Affine)
        
        # Coordenadas de las esquinas
        top_left = (transform.c, transform.f)  # Esquina superior izquierda
        top_right = (transform * (src.width, 0))  # Esquina superior derecha
        bottom_left = (transform * (0, src.height))  # Esquina inferior izquierda
        bottom_right = (transform * (src.width, src.height))  # Esquina inferior derecha
        
        # Dimensiones de la imagen
        width, height = src.width, src.height

        # Sistema de referencia espacial (CRS)
        crs = src.crs
        
        print("Metadata:")
        print("---------")
        for key, value in src.profile.items():
            print(f"{key}: {value}")
        
        print("\nCoordenadas de las esquinas de la imagen:")
        print("TOP LEFT:", top_left)
        print("BOTTOM RIGHT:", bottom_right)

        # Creación del diccionario
        img_dict['metadata'] = src.meta
        img_dict['top_left'] = top_left
        img_dict['top_right'] = top_right
        img_dict['bottom_left'] = bottom_left
        img_dict['bottom_right'] = bottom_right
        img_dict['width'] = width
        img_dict['height'] = height
        img_dict['crs'] = crs

        for key, value in src.profile.items():
            img_dict[key] = value

    return img_dict


def crop_tile_into_subrecortes(
        tiff_file: str,
        output_dir: str,
        coords_csv: str = './coords/yolo_coords.csv',
        tile_size: int = 640,
        overlap: int = 128,
        is_negative: bool = False
) -> None:
    """
    Recorta una imagen grande del ortomosaico en subrecortes de 640x640 píxeles con un solapamiento de 256 píxeles,
    guardando solo los recortes que contienen al menos una coordenada del archivo CSV.

    Args:
    - tiff_file: str - Ruta al archivo TIFF que se desea recortar.
    - output_dir: str - Directorio donde se guardarán los subrecortes.
    - coords_csv: str - Ruta al archivo CSV con las coordenadas (class, x_center, y_center, width, height).
    - tile_size: int - Tamaño de los subrecortes (por defecto 640).
    - overlap: int - Tamaño del solapamiento entre subrecortes (por defecto 256).
    - is_negative: bool - Si se deben guardar subrecortes sin coordenadas (por defecto False).
    """

    # Leer coordenadas del archivo CSV
    coords_df = pd.read_csv(coords_csv, header=None, names=["class", "x_center", "y_center", "width", "height"])
    coords_df["x_center"] = pd.to_numeric(coords_df["x_center"], errors="coerce")
    coords_df["y_center"] = pd.to_numeric(coords_df["y_center"], errors="coerce")

    # Eliminar filas con valores no numéricos
    coords_df = coords_df.dropna(subset=["x_center", "y_center"])

    # Obtener información de la imagen
    with rasterio.open(tiff_file) as src:
        WIDTH = src.width
        HEIGHT = src.height
        transform = src.transform  # Transformación geográfica de la imagen

    # Calcular el paso entre tiles considerando el solapamiento
    step = tile_size - overlap

    # Recorrer filas y columnas según el paso calculado
    with rasterio.open(tiff_file) as src:
        for upper in range(0, HEIGHT, step):
            for left in range(0, WIDTH, step):
                # Calcular los límites del recorte
                lower = min(upper + tile_size, HEIGHT)
                right = min(left + tile_size, WIDTH)

                # Crear ventana de recorte
                window = Window(left, upper, right - left, lower - upper)
                cropped_image = src.read(window=window)

                # Transformar los píxeles del recorte a coordenadas geográficas
                top_left_coords = rasterio.transform.xy(transform, upper, left, offset="ul")
                min_x, max_y = top_left_coords

                # Filtrar coordenadas dentro del recorte
                filtered_coords = coords_df[
                    (coords_df["x_center"] >= min_x) & (coords_df["x_center"] <= min_x + (right - left) * transform.a) &
                    (coords_df["y_center"] <= max_y) & (coords_df["y_center"] >= max_y - (lower - upper) * abs(transform.e))
                ]

                # Actualizar metadatos para el subrecorte
                cropped_meta = src.meta.copy()
                cropped_meta.update({
                    "height": lower - upper,
                    "width": right - left,
                    "transform": rasterio.windows.transform(window, src.transform)
                })

                # Guardar el recorte
                imagename = os.path.splitext(os.path.basename(tiff_file))[0]
                filename = f"{imagename}_{min_x}_{max_y}.tiff"
                output_path = os.path.join(output_dir, filename)

                if is_negative:
                    txt_output_dir = os.path.join("coords", "negatives")
                    os.makedirs(txt_output_dir, exist_ok=True)
                    if filtered_coords.empty:
                        with rasterio.open(output_path, 'w', **cropped_meta) as dst:
                            dst.write(cropped_image)
                        # Crear un txt vacío para cada imagen que cumpla esta condición
                        txt_file_path = os.path.join(txt_output_dir, os.path.basename(output_path).replace('.tiff', '.txt'))
                        with open(txt_file_path, 'w') as txt_file:
                            pass  
                else:
                    # Solo guardar si hay coordenadas y si la imagen tiene 640px
                    if filtered_coords.empty or cropped_image.shape[1] != 640 or cropped_image.shape[2] != 640:
                        continue  

                        
                    with rasterio.open(output_path, 'w', **cropped_meta) as dst:
                        dst.write(cropped_image)
