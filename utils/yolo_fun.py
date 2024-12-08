
import os
import pandas as pd
from tqdm import tqdm  
import rasterio


def hello():
    print("Hello, world!")



def generar_txt_yolo(
    subrecorte_dir: str, 
    csv_file: str = 'coords/yolo_coords.csv',  # Asegúrate de que este archivo tenga las coordenadas no normalizadas
    coords_dir: str = 'coords/labels_sin_normalizar'  # Directorio donde se guardarán los archivos .txt generados
) -> pd.DataFrame:
    """
    Genera archivos de etiquetas YOLO para cada tile basado en coordenadas no normalizadas.

    Args:
    - csv_file (str): Ruta al archivo CSV con las coordenadas no normalizadas.
    - subrecorte_dir (str): Directorio donde están las imágenes recortadas.
    - coords_dir (str): Directorio donde se guardarán los archivos .txt generados.
    """
    # Cargar el CSV con las coordenadas no normalizadas
    data = pd.read_csv(csv_file, header=None, names=['class', 'x_center', 'y_center', 'width', 'height'])

    # Convertir las columnas a tipos numéricos
    data = data.drop(index=0)

    data['x_center'] = pd.to_numeric(data['x_center'])
    data['y_center'] = pd.to_numeric(data['y_center'])
    data['width'] = pd.to_numeric(data['width'])
    data['height'] = pd.to_numeric(data['height'])

    # Asegurarse de que el directorio de salida existe
    os.makedirs(coords_dir, exist_ok=True)
    
    # Obtener los nombres de las imágenes (tiles)
    image_files = [f for f in os.listdir(subrecorte_dir) if f.endswith(('.tif', '.png', '.tiff'))]

    for image_file in tqdm(image_files, desc="Generando archivos .txt"):
        image_path = os.path.join(subrecorte_dir, image_file)
        
        # Abrimos la imagen georeferenciada con rasterio
        with rasterio.open(image_path) as src:
            # Obtener las coordenadas geográficas de la imagen (bounding box)
            xmin, ymin, xmax, ymax = src.bounds  # Estos son los límites geográficos de la imagen

        # Filtrar las coordenadas que caen dentro de las coordenadas geográficas de la imagen
        filtered_data = data[
            (data['x_center'] >= xmin) & (data['x_center'] <= xmax) &
            (data['y_center'] >= ymin) & (data['y_center'] <= ymax)
        ]

        # Crear el archivo .txt para este tile
        if not filtered_data.empty:
            # Crear el archivo .txt para este tile
            output_path = os.path.join(coords_dir, f"{os.path.splitext(image_file)[0]}.txt")
            filtered_data[['class', 'x_center', 'y_center', 'width', 'height']].to_csv(
                output_path, sep=' ', index=False, header=False
            )

    print(f"Archivos .txt generados en {coords_dir}")
    return filtered_data







def normalize_yolo_coords(
    tiff_file: str,  
    coords_sin_normalizar: pd.DataFrame, 
    output_file: str,
) -> None:
    """
    Normaliza todas las coordenadas del dataset completo al formato YOLO.
    
    Args:
    - tiff_file: str - Ruta al archivo TIFF que define el área de referencia.
    - coords_sin_normalizar: pd.DataFrame - DataFrame con coordenadas (Id, x_center, y_center, width, height).
    - output_file: str - Nombre del archivo de salida con las coordenadas normalizadas.
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

    # Filtrar los puntos dentro del área total (opcional)
    coords_sin_normalizar = coords_sin_normalizar[
        (coords_sin_normalizar[1] >= min_x) & (coords_sin_normalizar[1] <= max_x) &
        (coords_sin_normalizar[2] >= min_y) & (coords_sin_normalizar[2] <= max_y)
    ]

    # Normalizar las coordenadas y dimensiones
    coords_sin_normalizar[1] = (coords_sin_normalizar[1] - min_x) / (max_x - min_x)  # Normalización en X
    coords_sin_normalizar[2] = (coords_sin_normalizar[2] - min_y) / (max_y - min_y)  # Normalización en Y
    coords_sin_normalizar[3] = coords_sin_normalizar[3] / width  # Normalización del ancho
    coords_sin_normalizar[4] = coords_sin_normalizar[4] / height  # Normalización de la altura

    # Guardar el dataset en formato YOLO
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    coords_sin_normalizar.to_csv(output_file, index=False, header=False, sep=' ')
