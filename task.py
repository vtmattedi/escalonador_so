import random
from enum import Enum
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
        self.estado = TaskState.PRONTO  # Estado inicial do processo
        self.taskFailed = False

    def tick(self, tempo):
        if self.duracao == self.restante:
            self.response_time = tempo - self.chegada
        if self.restante > 0:
            self.restante -= 1
        if tempo > self.deadline and self.restante > 0:
            self.taskFailed = True
        if self.restante == 0:
            self.turn_around_time = tempo - self.chegada
            self.estado = TaskState.FINALIZADO
    def __str__(self):
        return f"{self.nome} (Prioridade: {self.prioridade}, Chegada: {self.chegada}, Duração: {self.duracao}, Deadline: {self.deadline}, Estado: {self.estado})"