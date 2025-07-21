
import copy
import random
from abc import ABC, abstractmethod
from task import TaskState, task

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
        self.tickets = {}
        self.last_process = set()
    # Reorna um processo aleatório da lista de processos
    # Cada processo tem um número de tickets, que é decrementado a cada vez que o processo é selecionado
    # O numero incial de tickets é 10 - burst time do processo
    # O processo selecionado perde 1 ticket e os outros ganham 1 ticket.
    # Atualmente só funciona com sistema single core.
    def escalonar(self, processos):
        # adiciona novos processos à lista de tickets
        for p in processos:
            if p not in self.tickets:
                n_tickets = max(1, 10 - p.duracao)
                self.tickets[p] = n_tickets
                  
        # Remove processos que não estão mais na lista de processos
        self.tickets = {p: t for p, t in self.tickets.items() if p in processos}
        pool = [item for item, weight in self.tickets.items() for _ in range(weight)]
        res = []
        seen = set()
        for p in pool:
            if p not in seen: # set() > list() for search
                seen.add(p)
                res.append(p)
        if res:
            self.tickets[res[0]] -= 1 if self.tickets[res[0]] > 1 else 1  
            # decrementa o número de tickets do processo selecionado
        for p in processos:
            if p is not res[0]:
                self.tickets[p] += 1  # incrementa o número de tickets dos outros processos
        return res

class escalonador_hrrn(algoritimo_base):
    def __init__(self):
        super().__init__()
        self.name = "HRRN"

    def escalonar(self, processos):
        for p in processos:
            p.hrrn = (p.duracao + (p.wait_time if p.wait_time is not None else 0)) / p.duracao
        return sorted(processos, key=lambda p: (p.chegada, -p.hrrn))
