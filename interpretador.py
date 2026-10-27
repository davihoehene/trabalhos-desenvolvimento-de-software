import re
from dominio import Musica, Voz, EventoMusical

class InterpretadorDeTexto:
    def __init__(self):
        self.notas_base = {'C': 12, 'D': 14, 'E': 16, 'F': 17, 'G': 19, 'A': 21, 'B': 23}
        self.duracoes = {'1': 4.0, '2': 2.0, '3': 1.0, '4': 0.5, '5': 0.25, '6': 0.125, '7': 0.0625}
        self.configs_iniciais = [
            (6, 100, 6),  # Voz 0
            (5, 80, 20),  # Voz 1
            (4, 60, 0),   # Voz 2
            (3, 40, 70)   # Voz 3
        ]

    def processar_texto(self, texto: str, bpm_inicial: int) -> Musica:
        musica = Musica(bpm_global=bpm_inicial)
        linhas = texto.split('\n')
        
        for id_voz, linha in enumerate(linhas):
            if id_voz > 3: 
                break
                
            oitava, volume, instrumento = self.configs_iniciais[id_voz]
            voz = Voz(id_voz, oitava, volume, instrumento)
            
            match_atraso = re.match(r'^\s*\[(\d+)\]', linha)
            if match_atraso:
                voz.atraso_inicial_beats = int(match_atraso.group(1))
                linha = linha[match_atraso.end():]
                
            self._processar_linha(linha, voz, musica)
            musica.adicionar_voz(voz)
            
        return musica

    def _processar_linha(self, linha: str, voz: Voz, musica: Musica):
        oitava_atual = voz.oitava_base
        volume_atual = voz.volume_base
        instrumento_atual = voz.instrumento_base
        ultima_nota_midi = None
        anterior_foi_nota = False
        
        i = 0
        while i < len(linha):
            char = linha[i]
            processou_nota = False
            
            if char in self.notas_base:
                nota_midi = self.notas_base[char] + (oitava_atual * 12)
                acidente = 0
                duracao = 1.0
                
                if i + 1 < len(linha) and linha[i+1] in ['#', 'b']:
                    acidente = 1 if linha[i+1] == '#' else -1
                    i += 1
                    
                if i + 2 < len(linha) and linha[i+1] == ':' and linha[i+2] in self.duracoes:
                    duracao = self.duracoes[linha[i+2]]
                    i += 2
                    
                nota_midi += acidente
                evento = EventoMusical(nota_midi, duracao, volume_atual, instrumento_atual)
                voz.adicionar_evento(evento)
                ultima_nota_midi = nota_midi
                processou_nota = True
                
            elif char == '>':
                musica.bpm_global += 10
            elif char == '<':
                musica.bpm_global = max(10, musica.bpm_global - 10)
            elif char == '?':
                oitava_atual += 1
            elif char == 'V':
                oitava_atual -= 1
            elif char == ' ':
                volume_atual = min(127, volume_atual * 2)
            elif char == '!':
                instrumento_atual = 24
            elif char == ',':
                instrumento_atual = 114
            elif char == ';' or (char.isdigit() and int(char) % 2 != 0):
                instrumento_atual = 15
            elif char.isdigit() and int(char) % 2 == 0:
                instrumento_atual = (instrumento_atual + int(char)) % 128
            else:
                if char not in ['\n', 'b', '#', ':']:
                    if anterior_foi_nota and ultima_nota_midi is not None:
                        evento = EventoMusical(ultima_nota_midi, 1.0, volume_atual, instrumento_atual)
                        voz.adicionar_evento(evento)
                        processou_nota = True
                    else:
                        evento = EventoMusical(None, 1.0, 0, instrumento_atual) 
                        voz.adicionar_evento(evento)
            
            anterior_foi_nota = processou_nota
            i += 1