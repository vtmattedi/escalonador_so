
from snapshot import snapshot
from task import task, TaskState
import console
import os
import time

class Simulator():
    def __init__(self, escalonador, preemptable):
        super().__init__()
        self.processos_disponiveis = set()
        self.processos = set()
        self.tempo = 0
        self.escalonador = escalonador
        self.current_task = None
        self.preemptable = preemptable
        self.context_switches = 0

    def adicionar_processo(self, processo):
        self.processos.add(processo)
        if processo.chegada <= self.tempo:
            self.processos_disponiveis.add(processo)

    def tick(self):
        # Se o escalonador não for preemptável, não faz nada até a tarefa atual terminar
        if self.current_task is not None and not self.preemptable:
            pass
        else:
            # pede para o escalonador ordenar os processos disponíveis
            if self.current_task is not None:
                self.current_task.estado = TaskState.PRONTO
            p = self.escalonador.escalonar(self.processos_disponiveis)
            if p:
                # Isso faz com que escalar a mesma logica para mais processadores seja facil.
                # self.current_task seria uma lista de processos e 
                # pegaria N_CORES processos do escalonador
                if self.current_task != p[0]:
                    self.context_switches += 1
                self.current_task = p[0]
                self.current_task.estado = TaskState.EXECUTANDO
        self.tempo += 1
        if self.current_task is not None:
            self.current_task.tick(self.tempo)
            if self.current_task.estado == TaskState.FINALIZADO:
                self.processos_disponiveis.remove(self.current_task)
                self.current_task = None
        for job in self.processos:
            if self.tempo >= job.chegada and job not in self.processos_disponiveis and job.estado != TaskState.FINALIZADO:
                self.processos_disponiveis.add(job)
        print(self.current_task)

    def print_frame(self, frame):
        console.home()
        lcount = 0
        for line in frame.splitlines():
            console.fprint(line)
            lcount += 1
        for _ in range(os.get_terminal_size().lines - lcount):
            console.fprint("")
    def print_snapshot(self):
        frame = f"Algoritmo: {self.escalonador.__class__.__name__} Preemptivel: {self.preemptable}\n"
        frame += f"Tempo: {self.tempo}\n"
        frame += "Processos:\n"
        for p in self.processos:
            frame += f" - {p.nome}: {p.estado}\n"
        print(frame)
    def start_sync(self, sleep_time=0.5):
       def all_processes_finished():
            return all(p.estado == TaskState.FINALIZADO for p in self.processos)
       while not all_processes_finished():
           self.tick()
           self.print_snapshot()
           time.sleep(sleep_time)
    def calc_stat(self):
        total_waiting_time = 0
        total_turnaround_time = 0
        for p in self.processos:
            turnaround_time = p.restante + p.chegada
            waiting_time = turnaround_time - p.duracao
            total_waiting_time += waiting_time
            total_turnaround_time += turnaround_time
        avg_waiting_time = total_waiting_time / len(self.processos) if self.processos else 0
        avg_turnaround_time = total_turnaround_time / len(self.processos) if self.processos else 0
        return avg_waiting_time, avg_turnaround_time
if __name__ == "__main__":
    # Example usage
    sim = simulador()
    sim.adicionar_processo(task("Processo1", 0, 5, 10))
    sim.adicionar_processo(task("Processo2", 1, 3, 8))
    
    # Simulate a tick
    sim.tick()
    
    # Take a snapshot
    snap = sim.snapshot()
    print(f"Snapshot at time {snap.tempo}: {[p.nome for p in snap.processos]}")