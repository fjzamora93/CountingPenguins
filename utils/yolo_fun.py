
import os
import pandas as pd
from tqdm import tqdm  
import rasterio
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

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

    """
    Hay discrepancias entre el sistema de coordenadas utilizado y el que espera YOLO.
    Esta parte es necesario revisarla con cautela.
    """
    
    # Normalización corregida (con el flip en Y)
    coords_sin_normalizar.iloc[:, 1] = (coords_sin_normalizar.iloc[:, 1] - min_x) / (max_x - min_x)  # Normalización en X
    coords_sin_normalizar.iloc[:, 2] = (max_y - coords_sin_normalizar.iloc[:, 2]) / (max_y - min_y)  # Corregir Flip Vertical en Y
    coords_sin_normalizar.iloc[:, 3] = coords_sin_normalizar.iloc[:, 3] / width  # Normalización del ancho
    coords_sin_normalizar.iloc[:, 4] = coords_sin_normalizar.iloc[:, 4] / height  # Normalización de la altura

    # Guardar el dataset en formato YOLO
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    coords_sin_normalizar.to_csv(output_file, index=False, header=False, sep=' ')



#! NO FUNCIONA
def visualizar_cajas(
    imagen_path: str, 
    coords_normalizadas: pd.DataFrame, 
    ancho_imagen: int, 
    alto_imagen: int):
    """
    Visualiza las cajas delimitadoras normalizadas sobre la imagen.

    Args:
    - imagen_path: str - Ruta a la imagen.
    - coords_normalizadas: pd.DataFrame - DataFrame con columnas [x_center, y_center, width, height].
    - ancho_imagen: int - Ancho de la imagen en píxeles.
    - alto_imagen: int - Alto de la imagen en píxeles.
    """
    # Cargar la imagen
    imagen = Image.open(imagen_path)
    
    # Crear una figura de Matplotlib
    fig, ax = plt.subplots(1)
    ax.imshow(imagen)

    # Dibujar cada caja delimitadora
    for _, row in coords_normalizadas.iterrows():
        # Extraer coordenadas normalizadas
        x_center, y_center, width, height = row[0], row[1], row[2], row[3]

        # Convertir coordenadas normalizadas a píxeles
        x_center_px = x_center * ancho_imagen
        y_center_px = y_center * alto_imagen
        width_px = width * ancho_imagen
        height_px = height * alto_imagen

        # Calcular la esquina superior izquierda (top-left) de la caja
        top_left_x = x_center_px - (width_px / 2)
        top_left_y = y_center_px - (height_px / 2)

        # Dibujar el rectángulo
        rect = patches.Rectangle(
            (top_left_x, top_left_y), width_px, height_px, 
            linewidth=2, edgecolor='red', facecolor='none'
        )
        ax.add_patch(rect)

    # Mostrar la imagen con las cajas
    plt.show()


#! NO FUNCIONA
def draw_boxes(image_path, coords_df, box_width=30, box_height=30):
    """
    Dibuja cajas alrededor de las coordenadas dadas en un DataFrame sobre una imagen.
    Además, imprime las coordenadas de las esquinas superior izquierda e inferior derecha para depuración.

    Args:
        image_path (str): Ruta de la imagen.
        coords_df (pd.DataFrame): DataFrame sin encabezados con las coordenadas en formato [label, x, y, width, height].
        box_width (int): Ancho de las cajas (por defecto 30).
        box_height (int): Altura de las cajas (por defecto 30).
    """
    # Carga la imagen
    img = plt.imread(image_path)
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(img)
    
    # Obtener las dimensiones de la imagen
    img_height, img_width, _ = img.shape

    # Dibuja cada caja
    for _, row in coords_df.iterrows():
        x_center = row[1]  # Columna 1 es x
        y_center = row[2]  # Columna 2 es y
        
        # Convertir coordenadas del centro a las coordenadas de la esquina superior izquierda
        x = x_center - (box_width / 2)
        y = y_center - (box_height / 2)

        # Calcular las esquinas de la caja
        top_left_x = x
        top_left_y = y
        bottom_right_x = x + box_width
        bottom_right_y = y + box_height

        # Imprimir las coordenadas de las esquinas
        print(f"Esquinas de la caja:")
        print(f"  - Esquina superior izquierda: ({top_left_x}, {top_left_y})")
        print(f"  - Esquina inferior derecha: ({bottom_right_x}, {bottom_right_y})")
        
        # Verificar si la caja está dentro de los límites de la imagen
        if (top_left_x >= 0 and top_left_y >= 0 and 
            bottom_right_x <= img_width and bottom_right_y <= img_height):
            print("La caja está dentro de la imagen.")
        else:
            print("¡La caja está fuera de los límites de la imagen!")

        # Dibujar el rectángulo (caja)
        box = patches.Rectangle(
            (x, y), box_width, box_height,
            linewidth=1, edgecolor='red', facecolor='none'
        )
        ax.add_patch(box)

    plt.axis('off')
    plt.show()