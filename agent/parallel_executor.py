# agent/parallel_executor.py

from .executor import Executor

class ParallelExecutor:
    """
    Windows-safe: run tests sequentially.
    Parallel Playwright is NOT supported on Windows.
    """

    def __init__(self):
        self.executor = Executor()

    def run_parallel(self, list_of_actions_sets, settings=None):
        results = []

        for actions in list_of_actions_sets:
            results.append(self.executor.execute_actions(actions, settings=settings))

        return results
