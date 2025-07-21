from simulator import Simulator
import algoritimos
from task import task, taskStruct
import argparse
import os
import json
import console
# Algoritmos, Preemptabilidade
# Cada tupla contém o algoritmo e se é preemptável ou não

ALGORITMOS = [
    (algoritimos.escalonador_fcfs, True),
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
START_TASKS = [
    taskStruct("Processo1", chegada=0, duracao=5, prioridade=1, deadline=10),
    taskStruct("Processo2", chegada=1, duracao=3, prioridade=2, deadline=8),
    taskStruct("Processo3", chegada=2, duracao=2, prioridade=1, deadline=5),
    taskStruct("Processo4", chegada=3, duracao=4, prioridade=3, deadline=12),
    taskStruct("Processo5", chegada=4, duracao=1, prioridade=2, deadline=6)
]
CONTEXT_COST = 0.6  # Tempo de troca de contexto
TIME_SLICE = 1 # Tempo entre cada tick do escalonador
# Função para criar tarefas a partir de START_TASKS
# Nescessária para criar novas instâncias de task ao utilizar varios algoritmos
# Caso contrário, todas as instâncias de task seriam as mesmas e portatnto, teriam terminado apos a primeira execução
def create_tasks():
    tasks = []
    for i in range(len(START_TASKS)):
        tasks.append(task(**START_TASKS[i].__dict__))
    return tasks
if __name__ == "__main__":
    # Argumentos de linha de comando
    parser = argparse.ArgumentParser(description="Simulador de Escalonamento de Processos",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-t", type=float, default=0.5,
                        help="tempo de sleep entre ticks (padrão: 0.5) numeros negativos não são permitidos, 0 desativa o sleep"),
    parser.add_argument("-f", "--file", type=str, default="",
                        help="caminho para o arquivo de entrada")
    parser.add_argument("-o", "--output", type=str, default="",
                        help="caminho para o arquivo de saída (padrão: não salvar) !Cuidado, sobrescreve o arquivo se já existir!")
    parser.add_argument("-c", "--context-cost", type=float, default=CONTEXT_COST,
                        help="custo de troca de contexto (padrão: 0.6)")
    parser.add_argument("-ts", "--time-slice", type=float, default=TIME_SLICE,
                        help="tempo de slice do escalonador (padrão: 1)")
    args = parser.parse_args()
    data = []
    if args.context_cost is not None and args.context_cost >= 0:
        CONTEXT_COST = args.context_cost
    if args.time_slice is not None and args.time_slice > 0:
        TIME_SLICE = args.time_slice
    console.show_cursor(False)
    if args.file:
        args.file = args.file.strip()
        # Basic file validation
        if not os.path.isfile(args.file):
            print(f"Arquivo '{args.file}' não encontrado.")
            quit()
        if not args.file.endswith(".json"):
            print("Arquivo deve ser .json")
            quit()
        # Read tasks from file
        with open(args.file, "r") as f:
            file = json.load(f)
            if "tasks" in file:
                START_TASKS = []
                for t in file["tasks"]:
                    START_TASKS.append(taskStruct(**t))
            if "algoritmos" in file:
                ALGORITMOS = []
                for a in file["algoritmos"]:
                    ALGORITMOS.append((getattr(algoritimos, "escalonador_" + a["name"]), a["preemptable"]))
        print(ALGORITMOS, START_TASKS)     

    for alg, preemptable in ALGORITMOS:
        # print(f"Testando algoritmo: {alg.__name__}, Preemptável: {preemptable}")
        simulator = Simulator(alg(), preemptable, time_slice = TIME_SLICE)
        for _task in create_tasks():
            simulator.adicionar_processo(_task)
        simulator.start_sync(args.t if args.t >= 0 else 0.5)
        data.append((alg.__name__, preemptable, simulator.context_switches, simulator.calc_stat(CONTEXT_COST)))
        # simulator.start_sync()
        # simulator.print_snapshot()
    if args.output:
        print(f"\033[92;1mSalvando resultados em \033[4m{args.output}\033[0m")
        if not os.path.exists(args.output):
            with open(args.output, "w") as f:
                f.write("")
        else:
            os.remove(args.output)
            with open(args.output, "w") as f:
                f.write("")
    for _data in data:
        # console.home()
        print(f"Algoritmo: {_data[0]}, Preemptável: {_data[1]}, Trocas de Contexto: {_data[2]}")
        if args.output:
            with open(args.output, "a") as f:
                f.write(f"Algoritmo: {_data[0]}, Preemptavel: {_data[1]}, Trocas de Contexto: {_data[2]}\n")
                f.write(f"Estatisticas: {_data[3].safe_str()}\n")
    console.show_cursor(True)