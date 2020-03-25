import multiprocessing as mp

from src.task import Task
from src.data_access.wrapper.redis import RedisWrapper
from src.misc.config_manager import ConfigManager

config = ConfigManager()


class Server:
    """
    The Server is responsible for the allocation of tasks to the single worker
    """
    def __init__(self, redis_wrapper: RedisWrapper, queue_name: str = None):
        assert isinstance(redis_wrapper, RedisWrapper)
        if queue_name is not None:
            assert isinstance(queue_name, str)
        else:
            queue_name = config.get_value("FRONTEND_API_QUEUE")

        self.redis = redis_wrapper
        self.queue_name = queue_name

    def send_task_sync(self, task: Task, user_id: str, path_name: str):
        """
        puts a task to the queue and returns the results in the response

        :param task:
        :param user_id:
        :param path_name:
        :return:
        """
        result = self.put_task_on_queue_and_listen_channel(task)
        return result

    def send_task_async(self, task: Task, user_id: str, path_name: str):
        """
        puts a task to the queue and sends instantly an response. The actual result will be returned by a redis channel.

        :param task:
        :param user_id:
        :param path_name:
        :return:
        """

        def parallel_task(task, user_id: str, path_name: str):
            result = self.put_task_on_queue_and_listen_channel(task)
            self.redis.publish_to_channel(channel="{}_{}".format(path_name, user_id), value=result)

        p = mp.Process(target=parallel_task, args=(task, user_id, path_name))
        p.start()
        return {"status": "ok", "message": "calculation started!"}

    def put_task_on_queue_and_listen_channel(self, task: Task):
        """
        puts a task to the channel and listens for the response

        :param task:
        :return:
        """
        self.redis.put_on_queue(self.queue_name, task.serialize())

        def callback(data: dict):
            def wrapper(message):
                data["result"] = message
                return False
            return wrapper
        data = {}
        callback_function = callback(data)
        self.redis.subscribe_to_channel(channel="{}".format(task.id), callback_function=callback_function)
        print(data)
        return data