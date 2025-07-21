import copy
class snapshot:
    def __init__(self, processos, tempo, algoritimo=None, preemptable=None, context_switches=None, 
                 processos_disponiveis=None):
        self.escalonador = algoritimo.name
        self.preemptable = preemptable
        self.context_switches = context_switches
        self.processos_disponiveis = copy.deepcopy(processos_disponiveis)
        self.processos = copy.deepcopy(processos)
        self.tempo = tempo