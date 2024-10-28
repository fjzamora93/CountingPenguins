Una vez están clasificados los conjunto de entrenamiento y test, se procede a la ejecución de YOLO. Para ello, se debe seguir los siguientes pasos:

1. Creamos el archivo penguin_dataset.yaml, que tiene la configuración básica.
2. Ejecutar el siguiente comando en consola desde el directorio de yolov5

````bash
python train.py --img 640 --batch 16 --epochs 100 --data ../data/penguin_dataset.yaml --weights yolov5s.pt --name penguin_detection

//YOLOV7
python train.py --img 640 --batch 16 --epochs 100 --data ../data/penguin_dataset.yaml --cfg cfg/training/yolov7.yaml --weights 'yolov7.pt' --device cpu

````


### Paso 3: Evaluar el rendimiento
Una vez que el entrenamiento finalice, YOLOv5 generará un directorio de resultados con el nombre runs/train/penguin_detection, que contendrá:

weights/best.pt: Los pesos del mejor modelo, listos para usarse en detección.

### Gráficos de métricas de precisión, pérdida, etc., para evaluar el entrenamiento.
Paso 4: Realizar detecciones con el modelo entrenado
Para usar el modelo entrenado para hacer predicciones, puedes ejecutar:

```bash
python detect.py --weights runs/train/penguin_detection/weights/best.pt --img 640 --source data/images/val
```
