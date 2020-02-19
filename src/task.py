import uuid

POSSIBLE_TASKS = {
    "dummy": ["dummy_func"],
}


class Task:
    """
    Task is used by several subpackages to synchronize what to do between producer and consumer
    """
    def __init__(self, domain: str, function: str, arguments: dict):
        assert isinstance(domain, str)
        assert isinstance(function, str)
        assert isinstance(arguments, dict)
        assert domain in POSSIBLE_TASKS.keys(), "domain must be in possible domains. Check possible domains of " \
                                                "Task for help"
        assert function in POSSIBLE_TASKS[domain], " functions must be in pssoible functions for domain. Check method " \
                                                   "possible functions if you are uncertain!"
        self.domain = domain
        self.function = function
        self.arguments = arguments
        self.id = str(uuid.uuid1())

    @staticmethod
    def possible_domains() -> list:
        """
        lists the possible domains for a task

        :return:
        """
        print("Possible domains are ".join(POSSIBLE_TASKS.keys()))
        return list(POSSIBLE_TASKS.keys())

    @staticmethod
    def possible_functions(domain: str) -> list:
        """
        lists all possible functions for a specific domain

        :param domain: domain for which the functions should be listed
        :return:
        """
        assert isinstance(domain, str)
        assert domain in POSSIBLE_TASKS
        print("Possible functions are: ".join(POSSIBLE_TASKS[domain]))
        return POSSIBLE_TASKS[domain]

    def serialize(self):
        """
        serialized this task

        :return:
        """
        return {"domain": self.domain,
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
        assert all([key in task_keys for key in ["domain", "function", "arguments"]])
        task_cls = cls(domain=task["domain"], function=task["function"], arguments=task["arguments"])
        task_cls.id = task["id"]
        return task_cls
