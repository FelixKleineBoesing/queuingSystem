import pymongo
from pymongo import MongoClient


class MongoWrapper:

    __instance = None

    def __init__(self, host: str, port: int, user: str, password: str):
        if self.__class__.__instance is None:
            self.host = host
            self.port = port
            self.user = user
            self.password = password
            self.client = MongoClient(host=host, port=port, username=user, password=password)
            self.__class__.__instance = self
        else:
            raise ValueError("MongoWrapper is already initilaized. Get instance instead!")

    @classmethod
    def get_instance(cls):
        return cls.__instance

    def get_database(self, collection: str):
        return self.client[collection]

    def set(self, key: str, value):
        pass