
## Formato de coordenadas (notebook 3)



Para entrenar YOLOv8 correctamente, el archivo CSV o archivo de etiquetas debe estar en un formato que represente las cajas delimitadoras de tus objetos de la siguiente manera:

- Clase (id numérico de la clase del objeto)
- Centro de la caja en el eje x (cx)
- Centro de la caja en el eje y (cy)
- Ancho de la caja (w)
- Alto de la caja (h)

Dentro del csv quedaría así:

id, cx, cy, w, h



## Normalización de coordenadas

Dependiendo del modelo que elijas, deberás convertir las coordenadas en el formato específico que requieren los frameworks de entrenamiento. Para YOLO, las etiquetas deberían estar en un formato como [class_id, center_x, center_y, width, height] normalizado entre 0 y 1. 

[class_id, x_center, y_center, width, height]

**Puedes utilizar el archivo extract_coords.py para convertir las coordenadas de los archivos CSV a un formato normalizado.**
