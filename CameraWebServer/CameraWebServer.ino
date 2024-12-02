#include "esp_camera.h"
#include <WiFi.h>

// ============ Configurações do Modelo da Câmera ============
#define CAMERA_MODEL_AI_THINKER // Modelo AI-THINKER com PSRAM
#include "camera_pins.h"        // Definição dos pinos da câmera

// ============ Credenciais de WiFi ============
const char *ssid = "";
const char *password = "";

// Declaração de funções
void startCameraServer();

void setup() {
  Serial.begin(115200);
  Serial.println("\nInicializando...");

  // ============ Configuração da Câmera ============
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;     // Frequência do clock
  config.pixel_format = PIXFORMAT_JPEG; // Formato JPEG para streaming
  config.frame_size = FRAMESIZE_SVGA;  // Resolução 800x600
  config.jpeg_quality = 10;            // Qualidade JPEG (1 = alta, 63 = baixa)
  config.fb_count = 2;                 // Número de frames no buffer
  config.fb_location = CAMERA_FB_IN_PSRAM;

  // Inicializa a câmera
  if (esp_camera_init(&config) != ESP_OK) {
    Serial.println("Erro: Falha ao inicializar a câmera.");
    while (true); // Pausa o programa
  }

  // Configuração do sensor da câmera
  sensor_t *s = esp_camera_sensor_get();
  if (s) {
    s->set_vflip(s, 1);        // Corrige imagem de ponta-cabeça
    s->set_hmirror(s, 1);      // Espelha a imagem horizontalmente (esquerda-direita)
    s->set_brightness(s, 1);   // Aumenta o brilho
    s->set_saturation(s, -1);  // Reduz a saturação
  }

  // ============ Conexão WiFi ============
  WiFi.begin(ssid, password);
  WiFi.setSleep(false);

  Serial.print("Conectando ao WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado!");

  // Inicia o servidor da câmera
  startCameraServer();

  Serial.print("Camera Ready! Acesse: http://");
  Serial.println(WiFi.localIP());
}

void loop() {
  delay(10000); // Mantém o programa em execução
}
