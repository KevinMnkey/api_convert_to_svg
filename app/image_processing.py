import cv2
import numpy as np
import svgwrite
from io import BytesIO

def process_image_to_svg(image_bytes):
    # Convertir la imagen en un array numpy
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    # Aplicar un filtro mediano
    filtered_image = cv2.medianBlur(image, 5)

    # Binarizar la imagen
    _, binary_image = cv2.threshold(filtered_image, 128, 255, cv2.THRESH_BINARY)

    # Limpiar la imagen con morfología
    kernel = np.ones((5, 5), np.uint8)
    cleaned_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)

    # Detectar bordes usando Canny
    edges = cv2.Canny(cleaned_image, threshold1=50, threshold2=150)

    # Dilatar los bordes
    dilated_edges = cv2.dilate(edges, kernel, iterations=1)

    # Encontrar contornos
    contours, hierarchy = cv2.findContours(dilated_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Crear un archivo SVG en memoria
    dwg = svgwrite.Drawing(size=(image.shape[1], image.shape[0]))

    # Dibujar los contornos en el SVG
    for i, contour in enumerate(contours):
        if hierarchy[0][i][3] == -1:  # Solo contornos exteriores
            points = [(float(point[0][0]), float(point[0][1])) for point in contour]
            dwg.add(dwg.polygon(points, fill='black'))

    # Guardar el SVG en un objeto BytesIO
    svg_io = BytesIO()
    # Aquí es importante usar el modo binario
    svg_io.write(dwg.tostring().encode('utf-8'))
    svg_io.seek(0)

    return svg_io.getvalue()  # Retorna los bytes del SVG
