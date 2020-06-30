import unittest

from api.server import Server
from data_access.wrapper.redis import RedisWrapper


class ServerTester(unittest.TestCase):

    def test_construction(self):
        self.skipTest("Need to find a mock service for redis")
        redis_wrapper = RedisWrapper()
        server = Server(redis_wrapper=redis_wrapper)
        