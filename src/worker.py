import json
import multiprocessing as mp
import sys
import time

from src.data_access.wrapper.redis import RedisWrapper
from src.misc.config_manager import ConfigManager
from src.task import Task

config_manager = ConfigManager()


class Worker:

    def __init__(self, redis_wrapper: RedisWrapper):
        self.number_processes = config_manager.get_value("MAX_PROCESSES")
        self.semaphore = mp.Semaphore(self.number_processes)
        self.redis = redis_wrapper
        self.queue_name = config_manager.get_value("MAIN_API_QUEUE")
        self.critical_queue_name = config_manager.get_value("MAIN_API_QUEUE_CRITICAL")
        self._process_number_processes = {}
        self._processes = []
        self._current_number_processes = 0

    def run(self):
        """
        runs the worker which therefore listens to the redis queue and allocates the tasks

        """
        while True:
            msg = self.redis.get_from_queue(self.queue_name)
            if msg is not None and self._current_number_processes < self.number_processes:
                task_dict = json.loads(msg[1])
                task = Task.deserialize(task=task_dict)
                module = getattr(sys.modules[__name__], task.module)
                func = getattr(module, task.function)
                self.start_process(func=func, arguments=task.arguments, channel_id=task.id)
            time.sleep(0.5)

            indices_to_remove = [i for i, p in enumerate(self._processes) if not p.is_alive()]

            if len(indices_to_remove) > 0:
                for i in indices_to_remove:
                    self._current_number_processes -= self._process_number_processes[self._processes[i]]

            if len(indices_to_remove) > 0:
                for i in reversed(indices_to_remove):
                    del self._processes[i]

    def start_process(self, func, arguments, channel_id):
        """
        starts the specified task as a new process
        """

        def task(redis, target_func, semaphore, args, id):
            res = target_func(**args)
            redis.publish_to_channel(channel=id, value=res)
            semaphore.release()

        queue = mp.Queue()
        self.semaphore.acquire()
        p = mp.Process(target=task, args=(self.redis, func, self.semaphore, arguments, channel_id))
        p.start()
        number_processes = queue.get()
        self._processes.append(p)
        self._process_number_processes[p] = number_processes
        self._current_number_processes += number_processes


if __name__ == "__main__":
    redis = RedisWrapper(host=config_manager.get_value("REDIS_HOST"),
                         port=config_manager.get_value("REDIS_PORT"),
                         db=config_manager.get_value("REDIS_DB"))
