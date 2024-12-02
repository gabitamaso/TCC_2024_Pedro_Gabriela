import tkinter as tk
import pyautogui
from ocr_monitor import OCRMonitor


class Aplicacao:
    def __init__(self, root):
        """
        Inicializa a aplicação principal.

        Args:
            root (tk.Tk): Janela principal da interface Tkinter.
        """
        self.root = root
        self.root.title("Interface de Controle")
        self.root.geometry("900x800")
        self.posicao1 = None
        self.posicao2 = None
        self.monitor = None
        self.executando = False

        # Instância da classe OCRMonitor
        self.monitor_ocr = OCRMonitor(update_callback=self.atualizar_monitoramento)

        # Elementos da interface
        self._criar_widgets()

    def _criar_widgets(self):
        """
        Cria os elementos visuais da interface gráfica.
        """
        self.titulo = tk.Label(self.root, text="Automação Cicloergômetro", font=("Arial", 24, "bold"), fg="#004080")
        self.titulo.pack(pady=20)

        self.botao_calibrar = tk.Button(self.root, text="Calibrar Posições", command=self.calibrar_posicoes,
                                        font=("Arial", 16), width=20, height=2, bg="#004080", fg="white", relief="flat")
        self.botao_calibrar.pack(pady=10)

        self.botao_start_stop = tk.Button(self.root, text="Iniciar", command=self.toggle_processo,
                                          font=("Arial", 16), width=20, height=2, bg="#004080", fg="white", relief="flat")
        self.botao_start_stop.pack(pady=15)

        self.label_status = tk.Label(self.root, text="", font=("Arial", 12))
        self.label_status.pack(pady=15)

        self.monitoramento_text = tk.Text(self.root, height=10, width=80, wrap=tk.WORD, font=("Arial", 12), state=tk.DISABLED)
        self.monitoramento_text.pack(pady=10)

    def calibrar_posicoes(self):
        """
        Inicia o processo de calibragem, instruindo o usuário a posicionar o mouse.
        """
        self.label_status.config(text="Calibrando... Coloque o mouse na posição 1 e pressione Enter.")
        self.root.bind('<Return>', self.capturar_posicao1)


    def capturar_posicao1(self, event):
        """
        Captura a primeira posição do mouse.

        Args:
            event (tk.Event): Evento associado ao pressionar a tecla Enter.
        """
        self.posicao1 = pyautogui.position()
        self.label_status.config(text="Posição 1 capturada. Coloque o mouse na posição 2 e pressione Enter.")
        self.root.bind('<Return>', self.capturar_posicao2)


    def capturar_posicao2(self, event):
        """
        Captura a segunda posição do mouse e define a área de monitoramento.

        Args:
            event (tk.Event): Evento associado ao pressionar a tecla Enter.
        """
        self.posicao2 = pyautogui.position()
        self.monitor = {"top": self.posicao1[1], "left": self.posicao1[0],
                        "width": self.posicao2[0] - self.posicao1[0], "height": self.posicao2[1] - self.posicao1[1]}
        self.monitor_ocr.set_monitor(self.monitor)
        self.label_status.config(text=f"Posições calibradas:\n{self.monitor}\n\nClique em Iniciar para começar.")
        self.root.unbind('<Return>')


    def toggle_processo(self):
        """
        Alterna entre iniciar e parar o monitoramento.
        """
        if self.executando:
            self.monitor_ocr.stop()
            self.executando = False
            self.botao_start_stop.config(text="Iniciar")
            self.label_status.config(text="Processo parado.")
        else:
            if not self.monitor:
                self.label_status.config(text="Calibre as posições antes de iniciar.")
                return
            self.monitor_ocr.start()
            self.executando = True
            self.botao_start_stop.config(text="Parar")
            self.label_status.config(text="Processo iniciado.")
            

    def atualizar_monitoramento(self, text):
        """
        Atualiza o campo de texto com mensagens de monitoramento.

        Args:
            text (str): Mensagem a ser exibida no campo de monitoramento.
        """
        self.monitoramento_text.config(state=tk.NORMAL)
        self.monitoramento_text.insert(tk.END, text + "\n")
        self.monitoramento_text.yview(tk.END)
        self.monitoramento_text.config(state=tk.DISABLED)
