import serial
import time


def configurar_serial(port, baud_rate):
    """
    Configura e inicializa a conexão serial com o ESP32.

    Args:
        port (str): Porta serial (ex: "COM3").
        baud_rate (int): Taxa de transmissão (ex: 9600).

    Returns:
        serial.Serial: Objeto de conexão serial configurado.
    """
    esp32 = serial.Serial(port, baud_rate, timeout=1)
    esp32.dtr = False  # Desativa DTR para evitar reset
    esp32.rts = False  # Desativa RTS para evitar reset
    esp32.reset_input_buffer()  # Limpa o buffer de entrada
    time.sleep(2)  # Aguarda o ESP32 estabilizar
    return esp32


def enviar_dados(esp32, dados):
    """
    Envia dados para o ESP32 via serial.

    Args:
        esp32 (serial.Serial): Objeto de conexão serial.
        dados (str): Dados a serem enviados.
    """
    try:
        esp32.write(f"{dados}\n".encode())  # Envia como bytes
        time.sleep(1.5)  # Aguarda resposta
    except Exception as e:
        print(f"Erro ao enviar dados: {e}")


def ler_resposta(esp32):
    """
    Lê a resposta do ESP32.
    Trata casos em que a resposta não está em UTF-8.

    Args:
        esp32 (serial.Serial): Objeto de conexão serial.

    Returns:
        str: Resposta lida do ESP32.
    """
    try:
        response = esp32.readline()
        return response.decode("utf-8", errors="replace").strip()
    except Exception as e:
        return f"Erro ao ler resposta: {e}"

