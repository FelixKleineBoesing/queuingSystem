from src.modelling.capacity_planning.simulations.custom.sim_parts import Process, Worker
from src.modelling.capacity_planning.simulations.custom.simulation import CallCenterSimulation


def run():
    processes = [Process(open_from=60 * 60 * 8, close_from=22 * 60 * 60, incoming_prob=[10],
                         patience_prob=[5], language="GERMAN", channel="PHONE")]

    workers = [Worker(work_begin=8 * 60 * 60, work_end=22 * 60 * 60, ahts=[180], channels=["CHAT", "PHONE"],
                      languages=["GERMAN"])]

    callcenter = CallCenterSimulation(open_time=60 * 60 * 8, closed_time=60 * 60 * 22, worker=workers,
                                      processes=processes, size_waiting_room=None)

    callcenter.run()


if __name__ == "__main__":
    run()