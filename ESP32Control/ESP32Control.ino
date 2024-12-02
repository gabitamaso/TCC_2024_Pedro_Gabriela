#define POSITIVE_PIN 5  // Pino para valores positivos
#define NEGATIVE_PIN 22   // Pino para valores negativos

void setup() {
  Serial.begin(9600);
  
  // Configuração dos pinos como saída
  pinMode(POSITIVE_PIN, OUTPUT);
  pinMode(NEGATIVE_PIN, OUTPUT);

  // Garante que ambos os LEDs iniciem apagados
  digitalWrite(POSITIVE_PIN, LOW); 
  digitalWrite(NEGATIVE_PIN, LOW); 
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    int numPiscos = input.toInt();

    if (numPiscos != 0) {
      Serial.print("Diferença recebida: ");
      Serial.println(numPiscos);

      // Determina qual LED piscar com base no valor recebido
      int Pin = (numPiscos > 0) ? POSITIVE_PIN : NEGATIVE_PIN;

      // Pisca o LED tantas vezes quanto o valor absoluto da diferença
      for (int i = 0; i < abs(numPiscos); i++) {
        digitalWrite(Pin, HIGH);    // Liga o LED
        delay(300);
        digitalWrite(Pin, LOW);   // Desliga o LED
        delay(300);
      }
    } else {
      Serial.println("Valor inválido ou diferença zero recebida.");
    }
  }
}
