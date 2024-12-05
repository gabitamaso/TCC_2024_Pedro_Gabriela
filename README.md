# Sistema Automatizado para Controle de Carga em Máquinas Fitness

Este repositório apresenta o desenvolvimento de um sistema automatizado para controle de carga em cicloergômetros de braço, projetado especialmente para exames ergométricos voltados a atletas paralímpicos e pacientes com deficiência física. O sistema combina hardware e software para criar uma solução eficiente, segura e adaptável, alinhada às necessidades médicas e operacionais.

---

## Objetivo do Projeto

O objetivo principal deste trabalho foi criar um sistema que:
- Automatize o controle de carga nos cicloergômetros.
- Preserve a integridade do equipamento original através de uma abordagem de controle externo.
- Garanta flexibilidade para futuras manutenções e expansões.

O projeto é uma contribuição relevante para a tecnologia assistiva, promovendo avanços na inclusão social e na qualidade dos testes ergométricos.

---

## Funcionalidades do Sistema

- **Controle Automatizado de Carga**: Ajuste automático da carga do cicloergômetro com base em protocolos médicos predefinidos.
- **Monitoramento Contínuo**: Integração de mecanismos para monitoramento constante durante os testes.
- **Interface Flexível**: Sistema de software com interface amigável para operação e controle.
- **Preservação do Equipamento Original**: Solução de controle externo que mantém a integridade do cicloergômetro.

---

## Estrutura do Repositório

```plaintext
.
├── CameraWebServer/       # Código relacionado ao servidor da câmera ESP32
├── ESP32Control/          # Scripts de controle para o ESP32
├── __pycache__/           # Arquivos de cache gerados pelo Python
├── utils/                 # Funções utilitárias, incluindo OCR e controle serial
│   ├── ocr_utils.py       # Funções para OCR e processamento de imagem
│   ├── serial_utils.py    # Controle e comunicação com dispositivos seriais
│   └── __init__.py        # Arquivo para tornar a pasta um módulo Python
├── app.py                 # Ponto de entrada do sistema principal
├── interface.py           # Interface do usuário para controle e monitoramento
├── ocr_monitor.py         # Monitoramento do OCR em tempo real
├── teste_cam.py           # Script de teste para captura de imagem com ESP32

```

---

## Resultados

Os resultados do sistema demonstraram:

- **Viabilidade Técnica**: O sistema se mostrou funcional, com estabilidade nos ajustes automáticos.
- **Facilidade de Uso**: Interface simples e intuitiva para usuários médicos e técnicos.
- **Limitações**: Dependência de alguns componentes específicos, mas com possibilidade de substituições.

### Oportunidades de Melhoria

- **Integração de sensores adicionais**: Para ampliar as métricas disponíveis durante os exames.
- **Maior autonomia energética**: Uso de fontes de energia mais robustas para maior eficiência.
- **Ampliação de protocolos médicos suportados**: Adição de novos perfis e modos de operação.

---

## Dependências

Este projeto requer as seguintes bibliotecas para execução:

- **Python 3.8 ou superior**
- `opencv-python`
- `numpy`
- `pillow`
- `pytesseract`
- `requests`
- `mss`

---

## Autores

Este projeto foi desenvolvido por:

- **Gabriela Tamaso Pavani Agostini**
- **Pedro Sotelo Calvo**

---

## Considerações Finais

Este sistema representa uma contribuição significativa para a tecnologia assistiva e dispositivos médicos, promovendo avanços na inclusão social e na qualidade dos testes ergométricos. 

Com as melhorias planejadas, ele pode ser expandido para atender a uma gama ainda maior de necessidades médicas e operacionais, incluindo:
- A integração de sensores adicionais para melhorar a coleta de dados.
- O aumento da autonomia energética do sistema.
- A adição de novos protocolos médicos para maior personalização dos testes.

O projeto foi desenvolvido com foco na integração eficiente de hardware e software, garantindo:
- **Precisão nos testes**.
- **Facilidade de uso**.
- **Flexibilidade para manutenção e expansão futura**.

Este sistema tem o potencial de transformar a abordagem dos testes ergométricos, oferecendo uma solução inovadora para profissionais da área médica.
