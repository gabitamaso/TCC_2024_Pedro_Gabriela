import requests

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

# Configurações
url_camera = "http://192.168.15.13/capture"
caminho_foto = "foto_capturada.jpg"

# Captura a foto
capturar_foto(url_camera, caminho_foto)
