import uuid


class Task:
    """
    Task is used by several subpackages to synchronize what to do between producer and consumer
    """
    def __init__(self, module: str, function: str, arguments: dict):
        assert isinstance(module, str)
        assert isinstance(function, str)
        assert isinstance(arguments, dict)

        self.module = module
        self.function = function
        self.arguments = arguments
        self.id = str(uuid.uuid1())

    def serialize(self):
        """
        serialized this task

        :return:
        """
        return {"domain": self.module,
                "function": self.function,
                "arguments": self.arguments,
                "id": self.id}

    @classmethod
    def deserialize(cls, task: dict):
        """
        creates an instance of class Task from a serialized task

        :param task: serialized task
        :return:
        """
        assert isinstance(task, dict)
        task_keys = list(task.keys())
        assert all([key in task_keys for key in ["module", "function", "arguments"]])
        task_cls = cls(module=task["module"], function=task["function"], arguments=task["arguments"])
        task_cls.id = task["id"]
        return task_cls
