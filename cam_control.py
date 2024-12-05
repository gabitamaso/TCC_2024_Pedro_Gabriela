import requests
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def capturar_foto(url: str, caminho_arquivo: str) -> None:
    """
    Captura uma foto da câmera ESP32 com webserver e salva em um arquivo local.

    Args:
        url (str): URL do endpoint da câmera para capturar a foto.
        caminho_arquivo (str): Caminho onde a foto será salva (incluindo o nome do arquivo).

    Returns:
        None
    """
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(caminho_arquivo, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"Foto salva em: {caminho_arquivo}")
        else:
            print(f"Erro ao capturar foto. Código HTTP: {response.status_code}")
    except Exception as e:
        print(f"Erro ao acessar a câmera ESP32: {e}")



def process_image(image_path):
    # Carregar a imagem e cortá-la
    image = Image.open(image_path)
    image = np.array(image)
    cropped_image = image[260:410, 220:480]

    # Converter para escala de cinza
    gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

    # Aplicar filtro de desfoque
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Aplicar limiarização (threshold) e limpeza morfológica
    thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    cv2.imwrite("aaa2.png", thresh)
    image = cv2.imread('aaa2.png')
    x, y, x2, y2 = 128, 100, 148, 200  # Ajuste conforme necessário
    # Pintar a região com a cor desejada (por exemplo, azul)
    # Lembre-se: a ordem das cores no OpenCV é BGR (não RGB)
    image[y:y2, x:x2] = (0, 0, 0)  # Pintando de preto
    # Opcional: Salvar a imagem modificada

    # Definir as coordenadas das caixas de interesse (x, y, largura, altura)
    boxes = [
        (38, 0, 90, 145),  # Caixa 1
        (145, 0, 90, 145),  # Caixa 2
    ]

    for (x, y, w, h) in boxes:
    # Extrair a região de interesse (ROI)
        roi = gray[y:y+h, x:x+w]

        # Aplicar thresholding para binarizar a imagem (opcional)
        _, thresh = cv2.threshold(roi, 150, 255, cv2.THRESH_BINARY_INV)

        # Desenhar a caixa na imagem original
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Caixa verde

    # Mostrar os números extraídos
    #cv2.imwrite("aaa4.png", image)

    # Iterar sobre as caixas definidas

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar binarização (limiarização)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Encontrar contornos (assumindo que os retângulos estão bem definidos)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    digits = []  # Lista para armazenar os dígitos identificados

    # Iterar sobre os contornos encontrados
    for c in contours:
        # Ignorar pequenos contornos (ruídos)
        if cv2.contourArea(c) < 100:
            continue

        # Obter o retângulo delimitador do contorno
        (x, y, w, h) = cv2.boundingRect(c)

        # Garantir que estamos lidando com um retângulo proporcional a um dígito
        aspect_ratio = w / float(h)
        if aspect_ratio < 0.2 or aspect_ratio > 1.2:
            continue

        # Extrair a Região de Interesse (ROI)
        roi = thresh[y:y + h, x:x + w]

        # Dimensões do ROI
        (roiH, roiW) = roi.shape
        (dW, dH) = (int(roiW * 0.25), int(roiH * 0.15))
        dHC = int(roiH * 0.05)

        # Definir os segmentos
        segments = [
            ((0, 0), (w, dH)),                 # Top
            ((0, 0), (dW, h // 2)),           # Top-left
            ((w - dW, 0), (w, h // 2)),       # Top-right
            ((0, (h // 2) - dHC), (w, (h // 2) + dHC)),  # Center
            ((0, h // 2), (dW, h)),           # Bottom-left
            ((w - dW, h // 2), (w, h)),       # Bottom-right
            ((0, h - dH), (w, h))             # Bottom
        ]

        # Identificar segmentos acesos
        on = [0] * len(segments)
        for i, ((xA, yA), (xB, yB)) in enumerate(segments):
            segROI = roi[yA:yB, xA:xB]
            total = cv2.countNonZero(segROI)
            area = (xB - xA) * (yB - yA)
            if total / float(area) > 0.5:  # Se mais de 50% da área estiver preenchida
                on[i] = 1

        # Mapeamento de segmentos para dígitos
        DIGITS_LOOKUP = {
            (1, 1, 1, 0, 1, 1, 1): 0,
            (0, 0, 1, 0, 0, 1, 0): 1,
            (1, 0, 1, 1, 1, 0, 1): 2,
            (1, 0, 1, 1, 0, 1, 1): 3,
            (0, 1, 1, 1, 0, 1, 0): 4,
            (1, 1, 0, 1, 0, 1, 1): 5,
            (1, 1, 0, 1, 1, 1, 1): 6,
            (1, 0, 1, 0, 0, 1, 0): 7,
            (1, 1, 1, 1, 1, 1, 1): 8,
            (1, 1, 1, 1, 0, 1, 1): 9
        }

        # Verificar se o padrão de segmentos corresponde a algum dígito
        digit = DIGITS_LOOKUP.get(tuple(on), 4)  # -1 se o padrão não for encontrado
        digits.append(digit)

    numero_identificado = int("".join(map(str, digits)))

    return numero_identificado