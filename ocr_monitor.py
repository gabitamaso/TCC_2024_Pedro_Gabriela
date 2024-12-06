import time
import threading
from utils.ocr_utils import capturar_tela, extrair_numero
from utils.serial_utils import send_http_request
from cam_control import capturar_foto, process_image


class OCRMonitor:
    def __init__(self, esp_url = "http://192.168.15.7", update_callback=None):
        """
        Inicializa o monitor OCR e configura a comunicação com o ESP32 via Wi-Fi.

        Args:
            esp_url (str): URL base do ESP32 (ex: "http://192.168.15.7").
            update_callback (callable): Função de callback para atualizar textos de monitoramento.
        """
        self.monitor = None
        self.last_value = None
        self.running = False
        self.esp_url = esp_url
        self.update_callback = update_callback


    def set_monitor(self, monitor):
        """
        Define a região da tela para monitoramento.

        Args:
            monitor (dict): Região da tela (ex: {"top": 0, "left": 0, "width": 100, "height": 100}).
        """
        self.monitor = monitor


    def get_number(self):
        """
        Captura a tela e extrai o número visível usando OCR.

        Returns:
            int or None: Número extraído da tela, ou None se não encontrado.
        """
        if not self.monitor:
            return None
        img = capturar_tela(self.monitor)  # Usa o utilitário de captura de tela
        return extrair_numero(img)  # Usa o utilitário de OCR


    def send_to_esp32(self, difference, current_value):
        """
        Envia a diferença de valores ao ESP32 e gerencia o loop de ajuste via câmera.

        Args:
            difference (int): Diferença a ser enviada ao ESP32.
            current_value (int): Valor atual para comparação.
        """
        self._update_monitoring_text(f"Enviando diferença via Wi-Fi: {difference}")
        response = send_http_request(self.esp_url, "piscar", {"valor": difference})
        self._update_monitoring_text(f"Resposta ESP32: {response}")

        time.sleep(5)

        capturar_foto("url", "foto.png")
        numero_identificado = process_image("foto.png")

        new_difference = numero_identificado - current_value
        if new_difference != 0:
            self._update_monitoring_text(f"Enviando nova diferença - CAM: {new_difference}")
            response = self._send_http_request("piscar", {"valor": new_difference})
            self._update_monitoring_text(f"Resposta ESP32 - CAM: {response}")
        else:
            self._update_monitoring_text(f"Nenhuma diferença detectada")


    def _update_monitoring_text(self, text):
        """
        Atualiza o texto de monitoramento via callback.

        Args:
            text (str): Mensagem a ser exibida.
        """
        if self.update_callback:
            self.update_callback(text)


    def start(self):
        """
        Inicia o monitoramento em um thread separado.
        """
        if not self.running:
            self.running = True
            threading.Thread(target=self.monitor_loop, daemon=True).start()


    def stop(self):
        self.running = False


    def monitor_loop(self):
        """
        Loop principal para capturar, processar e enviar dados ao ESP32.
        """
        while self.running:
            current_value = self.get_number()
            if current_value is not None and current_value != self.last_value:
                difference = current_value - self.last_value if self.last_value is not None else 0
                self.send_to_esp32(difference, current_value)
                self.last_value = current_value
            time.sleep(4)
