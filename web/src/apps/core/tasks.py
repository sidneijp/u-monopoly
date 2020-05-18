from django_rq import job

from .simulation import SimulationRunner


@job
def run_simulation(simulation):
    runner = SimulationRunner(simulation)
    runner.run()
