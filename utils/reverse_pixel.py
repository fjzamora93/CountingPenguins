
import os
import csv

import pandas as pd
import rasterio 



def denormalize_yolo_coords(
    tiff_file: str,
    coords_normalizadas: pd.DataFrame,
    output_file: str,
) -> None:
    """
    Denormaliza las coordenadas del formato YOLO a su escala original.
    
    Args:
    - tiff_file: str - Ruta al archivo TIFF que define el área de referencia.
    - coords_normalizadas: pd.DataFrame - DataFrame con coordenadas normalizadas (Id, x_center, y_center, width, height).
    - output_file: str - Nombre del archivo de salida con las coordenadas denormalizadas.
    """
    # Abrir el archivo TIFF para obtener metadatos
    with rasterio.open(tiff_file) as src:
        transform = src.transform
        width, height = src.width, src.height

        # Definir los límites del área total
        top_left = transform * (0, 0)
        bottom_right = transform * (src.width, src.height)
        min_x, max_y = top_left
        max_x, min_y = bottom_right

    # Denormalizar las coordenadas
    coords_denormalizadas = coords_normalizadas.copy()

    coords_denormalizadas.iloc[:, 1] = coords_normalizadas.iloc[:, 1] * (max_x - min_x) + min_x  # Denormalizar X
    coords_denormalizadas.iloc[:, 2] = max_y - (coords_normalizadas.iloc[:, 2] * (max_y - min_y))  # Denormalizar Y y corregir flip
    coords_denormalizadas.iloc[:, 3] = coords_normalizadas.iloc[:, 3] * width  # Denormalizar ancho
    coords_denormalizadas.iloc[:, 4] = coords_normalizadas.iloc[:, 4] * height  # Denormalizar altura

    # Guardar el dataset denormalizado
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    coords_denormalizadas.to_csv(output_file, index=False, header=False, sep=' ')







# # Función para convertir píxeles a coordenadas geográficas
# def pixel_to_coordinates(
#     tile_name:str, 
#     pixel_x:int, 
#     pixel_y:int, 
#     csv_corners_data: str = os.path.join(settings.BASE_DIR, 'static', 'data', 'ortho_coordinates.csv'),
#     path_tiff_files: str = os.path.join(settings.BASE_DIR, 'static', 'img')
# ):
#     """
#     Esta función está pensada para llamarse dentro de un bucle for donde se itere 
#     sobre el JSON con todos los tiles con los píxeles marcados.

#     Convierte las coordenadas del píxel (pixel_x, pixel_y) de una imagen (tile) a coordenadas geográficas
#     usando la información de los límites geográficos (upper_left, bottom_right) que se encuentra en el CSV.
    
#     Args:
#     - tile_name (str): Nombre de la imagen/fragmento del ortomosaico.
#     - pixel_x (int): Posición X del píxel marcado en la imagen.
#     - pixel_y (int): Posición Y del píxel marcado en la imagen.
#     - csv_corners_data (str): Ruta al archivo CSV con las coordenadas de las esquinas de las imágenes.
#     - path_img_files: path a donde se encuentran las imágenes para medir su ancho y alto.
    
#     Returns:
#     - tuple: Coordenadas geográficas (x, y).
#     """
#     df_corners = pd.read_csv(csv_corners_data)

#     # Verificar si el tile_name está en el DataFrame
#     if tile_name not in df_corners['file'].values:
#         raise ValueError(f"El tile '{tile_name}' no se encuentra en el archivo CSV.")

#     # Obtener la fila correspondiente al tile
#     tile_row = df_corners[df_corners['file'] == tile_name].iloc[0]
#     x_top, y_top = tile_row['x_top'], tile_row['y_top']
#     x_bot, y_bot = tile_row['x_bot'], tile_row['y_bot']

#     # Construir la ruta al archivo TIFF
#     tiff_path = os.path.join(path_tiff_files, f"{tile_name}.tif")

#     # Obtener el ancho y alto de la imagen usando rasterio
#     with rasterio.open(tiff_path) as src:
#         width, height = src.width, src.height
#     print(f"Ancho de la imagen: {width} píxeles. Alto de la imagen: {height} píxeles")

#     # Calcular las proporciones de las coordenadas geográficas
#     x_ratio = pixel_x / width
#     y_ratio = pixel_y / height

#     # Calcular las coordenadas geográficas usando las proporciones
#     geo_x = x_top + x_ratio * (x_bot - x_top)
#     geo_y = y_top + y_ratio * (y_bot - y_top)

#     return geo_x, geo_y