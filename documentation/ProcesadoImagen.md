# Pasos  a seguir al tratar cada imagen y extraer coordenadas

1. Guardas la imagen troceada en una carpeta (debería estar dividido ya en tiles de 500x500)
2. Guardas las coordenadas -csv- dentro de la misma carpeta.
3. Procesar las coordenadas y normalizarlas (ejecutar el extract_coords.py o el ExtraccionMetadatosTile). Esto formateará las coordenadas para yolov8.... aunque tienes que averiguar en qué momento se separan los txt.

4. Cada tile -pequeño- tiene que tener un documento en txt con exactamente el mismo nombre y que contendrá solo las coordenadas de ese tile. Para ello, puedes ejecutar ClasificacionConjunto

- Comprobar de qué manera se corresponden las imagénes a las coordenadas, ¿cómo está organizado el tema?
- 