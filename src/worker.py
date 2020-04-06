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
        self._processes = []
        self._current_number_processes = 0

    def run(self):
        """
        runs the worker which therefore listens to the redis queue and allocates the tasks

        """
        while True:
            msg = self.redis.get_from_queue(self.queue_name)
            if msg is not None and self._current_number_processes < self.number_processes:
                queue = mp.Queue()
                task_dict = json.loads(msg[1])
                task = Task.deserialize(task=task_dict)
                module = getattr(sys.modules[__name__], task.module)
                func = getattr(module, task.function)
                self.semaphore.acquire()
                self.start_process(func=func, arguments=(task.arguments, queue), channel_id=task.id)
            time.sleep(0.5)

    def start_process(self, func, arguments, channel_id):
        """
        starts the specified task as a new process
        """

        def task(queue, target_func, semaphore, args, id):
            res = target_func(**args)
            queue.publish_to_channel(channel=id, value=res)
            semaphore.release()

        p = mp.Process(target=task, args=(self.redis, func, self.semaphore, arguments, channel_id))

        p.start()


if __name__ == "__main__":
    redis = RedisWrapper(host=config_manager.get_value("REDIS_HOST"),
                         port=config_manager.get_value("REDIS_PORT"),
                         db=config_manager.get_value("REDIS_DB"))
