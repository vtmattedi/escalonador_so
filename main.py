from simulator import Simulator
import algoritimos
from task import task
# Algoritmos, Preemptabilidade
# Cada tupla contém o algoritmo e se é preemptável ou não
ALGORITMOS = [
    (algoritimos.escalonador_fifo, True),
    (algoritimos.escalonador_sjf, True),
    (algoritimos.escalonador_rr, True),
    (algoritimos.escalonador_priority, True),
    (algoritimos.escalonador_edf, True),
    (algoritimos.escalonador_lottery, False),
    (algoritimos.escalonador_hrrn, True)
]

# task ("nome", chegada, burst, prioridade=0)

# Lista de tarefas iniciais
# Cada tupla contém (nome, chegada, duração, prioridade, deadline)
class taskStruct():
    def __init__(self, nome, chegada, duracao, prioridade=0, deadline=None):
        self.nome = nome
        self.chegada = chegada
        self.duracao = duracao
        self.prioridade = prioridade
        self.deadline = deadline if deadline is not None else chegada + duracao

START_TASKS = [
    taskStruct("Processo1", chegada=0, duracao=5, prioridade=1, deadline=10),
    taskStruct("Processo2", chegada=1, duracao=3, prioridade=2, deadline=8),
    taskStruct("Processo3", chegada=2, duracao=2, prioridade=1, deadline=5),
    taskStruct("Processo4", chegada=3, duracao=4, prioridade=3, deadline=12),
    taskStruct("Processo5", chegada=4, duracao=1, prioridade=2, deadline=6)
]

# Função para criar tarefas a partir de START_TASKS
# Nescessária para criar novas instâncias de task ao utilizar varios algoritmos
# Caso contrário, todas as instâncias de task seriam as mesmas e portatnto, teriam terminado apos a primeira execução
def create_tasks():
    tasks = []
    for i in range(len(START_TASKS)):
        tasks.append(task(*START_TASKS[i]))
    return tasks
if __name__ == "__main__":
    data = []
    for alg, preemptable in ALGORITMOS:
        print(f"Testando algoritmo: {alg.__name__}, Preemptável: {preemptable}")
        simulator = Simulator(alg(), preemptable)
        for _task in START_TASKS:
            simulator.adicionar_processo(_task)
        simulator.start_sync()
        data.append((alg.__name__, preemptable, simulator.context_switches, simulator.calc_stat()))
        
        # Aqui você pode adicionar processos ao simulador e iniciar a simulação
        # Exemplo:
        # simulator.adicionar_processo(task("Processo1", 0, 5))
        # simulator.start_sync()
        # simulator.print_snapshot()
    for _data in data:
        print(f"Algoritmo: {_data[0]}, Preemptável: {_data[1]}, Trocas de Contexto: {_data[2]}")
        # Aqui você pode processar os dados coletados, como salvar em um arquivo ou exibir estatísticas
        # Exemplo:
        # print(f"Estatísticas: {_data[3]}")