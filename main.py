import tkinter as tk
from tkinter import filedialog, messagebox
import os

# Importação das camadas de domínio e serviços construídas nas Tarefas 1, 2 e 3
from interpretador import InterpretadorDeTexto
from audio import ExportadorMIDI, ControladorDeAudio

class GerenciadorDeArquivos:
    @staticmethod
    def ler_texto(caminho_arquivo: str) -> str:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def guardar_texto(caminho_arquivo: str, conteudo: str):
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            f.write(conteudo)

class InterfaceGeradorMusical:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Música - Fase 2")
        self.root.geometry("600x500")

        self.interpretador = InterpretadorDeTexto()
        self.exportador = ExportadorMIDI()
        self.audio = ControladorDeAudio()

        self._construir_interface()

    def _construir_interface(self):
        # Barra de Ações (Ficheiros)
        frame_acoes = tk.Frame(self.root)
        frame_acoes.pack(pady=10)
        tk.Button(frame_acoes, text="Abrir TXT", command=self.abrir_txt).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_acoes, text="Guardar TXT", command=self.guardar_txt).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_acoes, text="Exportar MIDI", command=self.exportar_midi).pack(side=tk.LEFT, padx=5)

        # Configuração Global
        frame_config = tk.Frame(self.root)
        frame_config.pack(pady=5)
        tk.Label(frame_config, text="BPM Inicial Global:").pack(side=tk.LEFT)
        self.entrada_bpm = tk.Entry(frame_config, width=5)
        self.entrada_bpm.insert(0, "120")
        self.entrada_bpm.pack(side=tk.LEFT, padx=5)

        info_vozes = "(V0: Oit6/Cravo | V1: Oit5/Órgão | V2: Oit4/Piano | V3: Oit3/Fagote)"
        tk.Label(self.root, text=info_vozes, fg="gray").pack()

        # Área de Edição de Texto
        self.area_texto = tk.Text(self.root, height=15, width=70)
        self.area_texto.pack(pady=10)

        # Controlos de Reprodução
        frame_player = tk.Frame(self.root)
        frame_player.pack(pady=10)
        tk.Button(frame_player, text="GERAR E TOCAR", command=self.tocar_audio, bg="lightblue").pack(side=tk.LEFT, padx=5)
        tk.Button(frame_player, text="PARAR", command=self.parar_audio, bg="lightcoral").pack(side=tk.LEFT, padx=5)

        # Barra de Estado
        self.label_estado = tk.Label(self.root, text="Estado: Pronto.", fg="blue")
        self.label_estado.pack(side=tk.BOTTOM, pady=10)

    def _obter_musica_processada(self):
        texto = self.area_texto.get("1.0", tk.END).strip()
        try:
            bpm = int(self.entrada_bpm.get())
        except ValueError:
            bpm = 120
        return self.interpretador.processar_texto(texto, bpm)

    def abrir_txt(self):
        caminho = filedialog.askopenfilename(filetypes=[("Arquivos de Texto", "*.txt")])
        if caminho:
            conteudo = GerenciadorDeArquivos.ler_texto(caminho)
            self.area_texto.delete("1.0", tk.END)
            self.area_texto.insert(tk.END, conteudo)
            self.label_estado.config(text=f"Carregado: {os.path.basename(caminho)}")

    def guardar_txt(self):
        caminho = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivos de Texto", "*.txt")])
        if caminho:
            conteudo = self.area_texto.get("1.0", tk.END)
            GerenciadorDeArquivos.guardar_texto(caminho, conteudo)
            self.label_estado.config(text="Ficheiro TXT guardado com sucesso.")

    def exportar_midi(self):
        caminho = filedialog.asksaveasfilename(defaultextension=".mid", filetypes=[("Arquivos MIDI", "*.mid")])
        if caminho:
            musica = self._obter_musica_processada()
            self.exportador.gerar_arquivo(musica, caminho)
            self.label_estado.config(text="Ficheiro MIDI exportado com sucesso.")

    def tocar_audio(self):
        self.parar_audio()
        musica = self._obter_musica_processada()
        caminho_temp = "temp_playback.mid"
        self.exportador.gerar_arquivo(musica, caminho_temp)
        self.audio.tocar(caminho_temp)
        self.label_estado.config(text="A reproduzir áudio...")

    def parar_audio(self):
        self.audio.parar()
        self.label_estado.config(text="Reprodução parada.")

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceGeradorMusical(root)
    root.mainloop()