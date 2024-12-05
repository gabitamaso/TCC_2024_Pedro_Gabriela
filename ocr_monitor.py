import time
import threading
from utils.ocr_utils import capturar_tela, extrair_numero
from utils.serial_utils import configurar_serial, enviar_dados, ler_resposta
from cam_control import capturar_foto, process_image


class OCRMonitor:
    def __init__(self, esp_port="COM3", baud_rate=9600, update_callback=None):
        """
        Inicializa o monitor OCR e configura a comunicação serial com o ESP32.

        Args:
            esp_port (str): Porta serial para o ESP32.
            baud_rate (int): Taxa de transmissão da serial.
            update_callback (callable): Função de callback para atualizar textos de monitoramento.
        """        
        self.monitor = None
        self.last_value = None
        self.running = False
        self.esp32 = configurar_serial(esp_port, baud_rate)
        self.update_callback = update_callback


    def set_monitor(self, monitor):
        self.monitor = monitor


    def get_number(self):
        if not self.monitor:
            return None
        img = capturar_tela(self.monitor)  # Usa o utilitário de captura de tela
        return extrair_numero(img)  # Usa o utilitário de OCR


    def send_to_esp32(self, difference, current_value):
        self._update_monitoring_text(f"Enviando diferença: {difference}")
        enviar_dados(self.esp32, difference)  # Usa o utilitário de envio
        response = ler_resposta(self.esp32)  # Usa o utilitário de leitura
        self._update_monitoring_text(f"Resposta ESP32: {response}")
        time.sleep(5)
        capturar_foto("url", "foto.png")
        numero_identificado = process_image("foto.png")
        new_difference = numero_identificado - current_value
        if new_difference != 0:
            self._update_monitoring_text(f"Enviando diferença - CAM: {new_difference}")
            enviar_dados(self.esp32, new_difference)
            response = ler_resposta(self.esp32)  # Usa o utilitário de leitura
            self._update_monitoring_text(f"Resposta ESP32 - CAM: {response}")
        else:
            self._update_monitoring_text(f"Nenhuma diferença detectada")


    def _update_monitoring_text(self, text):
        if self.update_callback:
            self.update_callback(text)


    def start(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self.monitor_loop, daemon=True).start()


    def stop(self):
        self.running = False


    def monitor_loop(self):
        while self.running:
            current_value = self.get_number()
            if current_value is not None and current_value != self.last_value:
                difference = current_value - self.last_value if self.last_value is not None else 0
                self.send_to_esp32(difference, current_value)
                self.last_value = current_value
            time.sleep(4)
