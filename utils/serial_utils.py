import requests

def send_http_request(esp_url, endpoint, params):
    """
    Envia uma requisição HTTP ao ESP32.

    Args:
        esp_url (str): URL base do ESP32 (ex: "http://192.168.1.100").
        endpoint (str): Endpoint da rota (ex: "piscar").
        params (dict): Parâmetros a serem enviados na URL.

    Returns:
        str: Resposta do ESP32 ou mensagem de erro.
    """
    try:
        url = f"{esp_url}/{endpoint}"
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.text
        else:
            return f"Erro: Código de status {response.status_code}"
    except Exception as e:
        return f"Erro ao enviar requisição: {e}"
