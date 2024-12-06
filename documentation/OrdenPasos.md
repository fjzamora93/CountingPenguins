# Secuencia de pasos a seguir

- **Notebook 1**: Se recorta cada tile gigante (52, 62, etc) en tiles pequeñitos de 20 filas y 20 columnas (aproximadamente dará como resultado 500x500, aunque no exactamente).
- **Notebook 2**: OPCIONAL. Se extraen las coordenadas de cada tile y se guardan en coords_per_tile. Puesto que no es necesitamos las coordenadas de cada tile, sino de los subrecortes, este paso no es necesario.
- **Notebook 3**: Se asignan las labels en formato txt a cada pequeño subrecorte de 500x500 y se NORMALIZAN (segunda parte del notebook).
- **Notebook 4**: Se clasifican los conjuntos de train y val. Las imágenes provienen de cut_tiles. Las coordenadas están en coords.
- **Notebook 5**: Se entrena el modelo YOLOv5 con los datos de train y val.