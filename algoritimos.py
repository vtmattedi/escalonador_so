
import random
from abc import ABC, abstractmethod
from task import task

class algoritimo_base(ABC):
    def __init__(self):
        self.name_algoritmo = self.__class__.__name__

    @abstractmethod
    def escalonar(self, processos):
        """
        Método responsável por escalonar os processos.
        """
        raise NotImplementedError("Este método deve ser implementado por subclasses.")
    

class escalonador_fcfs(algoritimo_base):
    def __init__(self):
        super().__init__()
        self.name = "FCFS"

    def escalonar(self, processos):
        return sorted(processos, key=lambda p: p.chegada)

class escalonador_sjf(algoritimo_base):
    def __init__(self):
        super().__init__()
        self.name = "SJF"

    def escalonar(self, processos):
        # Ordena os processos por tempo restante
        # Caso não seja preemptivo, tempo restante = burst time
        return sorted(processos, key=lambda p: (p.restante, p.prioridade))

class escalonador_rr(algoritimo_base):
    def __init__(self):
        super().__init__()
        self.name = "RR"
        self.quantum = 1  # Tempo de quantum padrão
        self.fila = []
    def escalonar(self, processos):
        # Adiciona novos processos à fila
        for processo in processos:
            if processo not in self.fila:
                self.fila.append(processo)
        # Remove processos que não estão mais na lista de processos
        self.fila = [p for p in self.fila if p in processos]
        # retorna o primeiro processo da fila
        if self.fila:
            self.fila.append(self.fila.pop(0))  # Rotaciona o primeiro processo para o final
            
        return self.fila.copy()

    
class escalonador_priority(algoritimo_base):
    def __init__(self):
        super().__init__()
        self.name = "Priority"

    def escalonar(self, processos):
        # Ordena os processos por prioridade e tempo de chegada
        return sorted(processos, key=lambda p: (p.prioridade, p.chegada))

class escalonador_edf(algoritimo_base):
    def __init__(self):
        super().__init__()
        self.name = "EDF"

    def escalonar(self, processos):
        # Ordena os processos por deadline e prioridade
        return sorted(processos, key=lambda p: (p.deadline, p.prioridade))

class escalonador_lottery(algoritimo_base):
    def __init__(self):
        super().__init__()
        self.name = "Lottery"
    # Reorna um processo aleatório da lista de processos
    def escalonar(self, processos):
        if not processos:
            return None
        tickets = []
        for p in processos:
            n_tickets = max(1, 10 - p.duracao)  # Define o número de tickets baseado na duração
            tickets.extend([p] * n_tickets)
        random.shuffle(tickets)
        return tickets

class escalonador_hrrn(algoritimo_base):
    def __init__(self):
        super().__init__()
        self.name = "HRRN"

    def escalonar(self, processos):
        for p in processos:
            p.hrrn = (p.duracao + (p.wait_time if p.wait_time is not None else 0)) / p.duracao
        return sorted(processos, key=lambda p: (p.chegada, -p.hrrn))
