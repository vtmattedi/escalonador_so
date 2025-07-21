import random
from enum import Enum
class taskStruct():
    def __init__(self, nome, chegada, duracao, prioridade=0, deadline=None):
        self.nome = nome
        self.chegada = chegada
        self.duracao = duracao
        self.prioridade = prioridade
        self.deadline = deadline if deadline is not None else float('inf')  # Default to infinity if no deadline is provided

class TaskState(Enum):
    FUTURO = "futuro"
    PRONTO = "pronto"
    EXECUTANDO = "executando"
    FINALIZADO = "finalizado"
class task:
    def __init__(self, nome, chegada, duracao, deadline, prioridade=0):
        self.color = random.randint(0, 255)  # Random color for terminal output
        self.nome = nome
        self.prioridade = prioridade
        self.chegada = chegada
        self.duracao = duracao
        self.deadline = deadline
        self.restante = duracao
        self.response_time = None # Tempo de resposta 1ra execução
        self.turn_around_time = None # Tempo de retorno
        self.estado = TaskState.FUTURO  # Estado inicial do processo
        self.wait_time = None # Tempo de espera
        self.taskFailed = False
        # self.coreAfinity = None  # pinneToCore
        # self.softCoreAfinity = None  # set and managed by the SO to avoid task migration

    def tick(self, tempo, time_slice=1):
        if self.duracao == self.restante:
            self.response_time = tempo - self.chegada
        if self.restante > 0:
            self.restante -= time_slice
        if tempo > self.deadline and self.restante > 0:
            self.taskFailed = True
            self.estado = TaskState.FINALIZADO
            self.turn_around_time = tempo - self.chegada
            self.wait_time = self.turn_around_time - self.duracao + self.restante
        if self.restante == 0:
            self.turn_around_time = tempo - self.chegada
            self.wait_time = self.turn_around_time - self.duracao
            self.estado = TaskState.FINALIZADO

        return 
    def __str__(self):
        return f"{self.nome} (Prioridade: {self.prioridade}, Chegada: {self.chegada}, Duração: {self.duracao}, Deadline: {self.deadline}, Estado: {self.estado})"