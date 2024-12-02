from PIL import Image
import pytesseract
import mss


def capturar_tela(monitor):
    """
    Captura a tela dentro de uma região especificada.

    Args:
        monitor (dict): Região de captura (ex: {"top": 0, "left": 0, "width": 100, "height": 100}).

    Returns:
        PIL.Image: Imagem capturada.
    """
    with mss.mss() as sct:
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
        return img


def extrair_numero(img):
    """
    Extrai números de uma imagem usando OCR.

    Args:
        img (PIL.Image): Imagem a ser processada.

    Returns:
        int or None: Número extraído, ou None se não for encontrado.
    """
    text = pytesseract.image_to_string(img, config='--psm 7').strip()
    return int(text) if text.isdigit() else None
