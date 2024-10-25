
import os
import pandas as pd
import rasterio

CSV_FILE = os.path.join('tiles_coords', 'coords_62.csv')
IMGS_PATH = os.path.join('tiles_coords', 'subtiles')



def filtrar_datos_tile(csv_file: str, tiff_file: str, output_file_name: str) -> None:
    """
    Filtra los datos de un tile específico y los convierte al formato YOLO.
    
    Args:
    - csv_file: str - Ruta al archivo CSV con las coordenadas.
    - tiff_file: str - Ruta al archivo TIFF que define el área del tile.
    - output_file_name: str - Nombre del archivo de salida de etiquetas en formato YOLO.
    """
    # Cargar datos del CSV
    data = pd.read_csv(csv_file, encoding='ISO-8859-1')

    # Abrir el archivo TIFF y obtener los metadatos
    with rasterio.open(tiff_file) as src:
        transform = src.transform
        width, height = src.width, src.height
        
        # Definir los límites del tile
        top_left = transform * (0, 0)
        bottom_right = transform * (src.width, src.height)
        min_x, max_y = top_left
        max_x, min_y = bottom_right

    # Filtrar los puntos dentro del tile
    filtered_data = data[
        (data['x_center'] >= min_x) & (data['x_center'] <= max_x) &
        (data['y_center'] >= min_y) & (data['y_center'] <= max_y)
    ]

    print("X_center: ", data['x_center'], "Normalizado: " ((data['x_center'] - min_x) / width), 'Ancho: ', width)

    # Crear el DataFrame en el formato YOLO
    normalized_df = filtered_data.copy()
    normalized_df['class'] = normalized_df['class']  
    normalized_df['x_center'] = (normalized_df['x_center'] - min_x) / width
    normalized_df['y_center'] = (normalized_df['y_center'] - min_y) / height
    normalized_df['width'] = 30 / width  
    normalized_df['height'] = 30 / height

    # Guardar el archivo en el formato YOLO con espacios
    output_path = os.path.join('tiles_coords', 'labels', f'{output_file_name}.txt')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    normalized_df.to_csv(output_path, sep=' ', index=False, header=False)

    print(f"Archivo YOLO guardado en: {output_path}")


# Iterar sobre los archivos en el directorio de imágenes
for img in os.listdir(IMGS_PATH):
    if img.endswith('.tiff') or img.endswith('.tif'):  # Asegúrate de que solo procese archivos TIFF
        tiff_file = os.path.join(IMGS_PATH, img)
        filtrar_datos_tile(CSV_FILE, tiff_file, img.split('.')[0])