Una vez están clasificados los conjunto de entrenamiento y test, se procede a la ejecución de YOLO. Para ello, se debe seguir los siguientes pasos:

1. Creamos el archivo penguin_dataset.yaml, que tiene la configuración básica.
2. Creamos el sistema de directorios y subdirectorios para el entrenamiento y la validación.


Para empezar comenzamos organizando lso conjunjtos de train y test siguiendo esta estructura (esta estructura debe coincidir con la que definamos en el documento de settings de ultralytics).

```bash
datasets/
├── penguin_dataset.yaml
├── penguin_dataset/
    ├── images/
    │   ├── train/
    │   │   ├── 000001.jpg
    │   │   ├── 000002.jpg
    │   ├── val/
    │   │   ├── 000001.jpg
    │   │   ├── 000002.jpg
    ├── labels/
    |   │   ├── train/
    │   │   ├── 000001.jpg
    │   │   ├── 000002.jpg
    │   ├── val/
    │   │   ├── 000001.jpg
    │   │   ├── 000002.jpg
```

# Instalación de dependencias

Comenzamos instalando las dependencias necesarias para el entrenamiento de Yolov8. Para ello, ejecutamos el siguiente comando:

```bash
pip install ultralytics

# o si queremos actualizar la librería
pip upgrade ultralytics
```


# Comprobación de directorios

Si estamos trabajando con Yolov8, y tras instalar ultralytics, se va a generar un documento settings.json en el siguiente directorio de Ultralytics.

```bash

C:\Users\Administrador.CRISASUSESTUDIO\AppData\Roaming\Ultralytics
    
```

Dentro ese directorio encontraremos información ESENCIAL sobre donde se van a buscar las carpetas y los distintos subconjuntos:

```json
  "datasets_dir": "C:\\Users\\Administrador.CRISASUSESTUDIO\\Desktop\\projects\\CountingPenguins\\datasets",
  "weights_dir": "C:\\Users\\Administrador.CRISASUSESTUDIO\\Desktop\\projects\\CountingPenguins\\weights",
  "runs_dir": "C:\\Users\\Administrador.CRISASUSESTUDIO\\Desktop\\projects\\CountingPenguins\\runs",
```

## Ejecución del comando de entrenamiento

Ahora que está todo organizado, podemos ejecutar el comando.

**yolov8**
```bash
yolo train model=yolov8n.pt data=./datasets/penguin_dataset.yaml epochs=100 imgsz=500 batch=16 device=cpu
```

## Carpetas weights y runs

1. weights_dir: Aquí se guardan los pesos entrenados del modelo. Al ejecutar un entrenamiento, el modelo guardará los pesos del mejor modelo (por defecto, al final de cada época).

2. runs_dir: Esta carpeta almacena los resultados de las ejecuciones, como las métricas, los gráficos y otros registros del entrenamiento. Además, guarda un subdirectorio para cada ejecución con un identificador único (por ejemplo, exp seguido de un número).

Para asegurarse de que después de cada entreanmiento los resultados son completamente nuevos, es posible borrar el contenido de estas carpetas manualmetne sin problemas, o ejecutando estos comandos:

```bash
rm -r C:\Users\Administrador.CRISASUSESTUDIO\Desktop\projects\CountingPenguins\weights\*
rm -r C:\Users\Administrador.CRISASUSESTUDIO\Desktop\projects\CountingPenguins\runs\*
```

## Realizar nuevas predicciones

Para realizar nuevas predicciones, se puede ejecutar el siguiente comando:

datasets/penguin_dataset/images/train

```bash
yolo detect predict model=runs/detect/train/weights/best.pt source=./test_images

# Para guardar las métricas

yolo detect predict model=runs/detect/train5/weights/best.pt source=./datasets/penguin_dataset/images/train save_txt=True
yolo detect predict model=runs/detect/train5/weights/best.pt source=./datasets/penguin_dataset/images/val save_txt=True

```
- model=runs/detect/train/weights/best.pt: Esta es la ruta al modelo entrenado, específicamente el mejor modelo guardado (best.pt), que está en la carpeta de runs/detect/train/weights. Si tienes otro archivo de pesos que deseas usar, reemplaza la ruta.

- source=./test_images: Especifica la carpeta donde están las imágenes que quieres probar. En este caso, las imágenes están en ./test_images. Si están en otro lugar, solo cambia la ruta.

### Visualización de los resultados: 
Después de ejecutar el comando, YOLOv8 generará las predicciones y las almacenará en una subcarpeta dentro de runs/detect/predict/. Los resultados incluyen las imágenes con las predicciones y las cajas delimitadoras (bounding boxes).

### Ver los resultados: 
Los resultados estarán en la carpeta de salida que se crea automáticamente, como runs/detect/predict/exp, donde exp será un número de experimento (si es la primera vez que ejecutas este comando).




**VERSIONES ANTIGUAS -NO USAR**
````bash
python train.py --img 640 --batch 16 --epochs 100 --data ../data/penguin_dataset.yaml --weights yolov5s.pt --name penguin_detection

//YOLOV7
python train.py --img 640 --batch 16 --epochs 100 --data ../data/penguin_dataset.yaml --cfg cfg/training/yolov7.yaml --weights 'yolov7.pt' --device cpu

````