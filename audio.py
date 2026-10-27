from midiutil import MIDIFile
import pygame
from dominio import Musica

class ExportadorMIDI:
    def gerar_arquivo(self, musica: Musica, caminho_arquivo: str):
        # Cria o arquivo MIDI com o número de tracks igual ao número de vozes
        num_vozes = len(musica.vozes)
        if num_vozes == 0:
            return

        midi = MIDIFile(num_vozes)
        
        # O BPM global é definido no tempo 0 da primeira track
        midi.addTempo(0, 0, musica.bpm_global)

        for voz in musica.vozes:
            track = voz.id_voz
            canal = track # Aloca cada voz num canal MIDI independente
            
            midi.addTrackName(track, 0, f"Voz {track}")
            
            # O tempo cronológico da voz inicia com o atraso especificado pelo usuário
            tempo_atual = float(voz.atraso_inicial_beats)
            instrumento_corrente = voz.instrumento_base
            
            # Configura o instrumento base no instante 0 da track
            midi.addProgramChange(track, canal, 0, instrumento_corrente)
            
            for evento in voz.eventos:
                # Trata mudanças dinâmicas de instrumento ao longo da linha
                if evento.instrumento != instrumento_corrente:
                    instrumento_corrente = evento.instrumento
                    midi.addProgramChange(track, canal, tempo_atual, instrumento_corrente)
                
                # Se for uma nota válida (diferente de None/Pausa), adiciona ao arquivo
                if evento.nota_midi is not None:
                    midi.addNote(track, canal, evento.nota_midi, tempo_atual, evento.duracao_beats, evento.volume)
                
                # O relógio avança obrigatoriamente com a duração do evento, seja nota ou pausa
                tempo_atual += evento.duracao_beats

        with open(caminho_arquivo, "wb") as arquivo_saida:
            midi.writeFile(arquivo_saida)

class ControladorDeAudio:
    def __init__(self):
        pygame.mixer.init()

    def tocar(self, caminho_arquivo: str):
        try:
            pygame.mixer.music.load(caminho_arquivo)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Erro ao reproduzir áudio: {e}")

    def parar(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()