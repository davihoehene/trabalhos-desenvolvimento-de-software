class EventoMusical:
    def __init__(self, nota_midi: int, duracao_beats: float, volume: int, instrumento: int):
        self.nota_midi = nota_midi
        self.duracao_beats = duracao_beats
        self.volume = volume
        self.instrumento = instrumento

class Voz:
    def __init__(self, id_voz: int, oitava_base: int, volume_base: int, instrumento_base: int):
        self.id_voz = id_voz
        self.oitava_base = oitava_base
        self.volume_base = volume_base
        self.instrumento_base = instrumento_base
        self.atraso_inicial_beats = 0
        self.eventos = []

    def adicionar_evento(self, evento: EventoMusical):
        self.eventos.append(evento)

class Musica:
    def __init__(self, bpm_global: int = 120):
        self.bpm_global = bpm_global
        self.vozes = []

    def adicionar_voz(self, voz: Voz):
        self.vozes.append(voz)