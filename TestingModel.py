import torch
from pathlib import Path
from PIL import Image

# Ruta al modelo YOLOv5 y directorio de imágenes
model_path = './best.pt'  # Usando string para la ruta

# Intentar cargar el modelo YOLOv5 directamente
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)

image_dir = './data/images/val'

# Iterar sobre las imágenes en el directorio
for image_path in Path(image_dir).rglob('*'):
    if image_path.suffix in ['.jpg', '.png', '.jpeg', '.tiff']:
        # Realizar predicción
        img = Image.open(image_path)  # Abre la imagen usando PIL
        results = model(img)  # Realiza la predicción
        
        # Guardar resultados (esto guardará las imágenes con las predicciones)
        results.save()  # Guardará las imágenes con predicciones en `runs/detect`
        print(f"Procesada: {image_path.name}")
