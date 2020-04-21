import abc

from src.data_access.wrapper.mongo import MongoWrapper
from src.data_access.wrapper.postgres import PostgresWrapper
from src.data_access.wrapper.redis import RedisWrapper


class BaseDataAccessor(abc.ABC):

    def __init__(self, mongo_wrapper: MongoWrapper, postgres_wrapper: PostgresWrapper, redis_wrapper: RedisWrapper):
        self.mongo = mongo_wrapper
        self.postgres = postgres_wrapper
        self.redis = redis_wrapper

