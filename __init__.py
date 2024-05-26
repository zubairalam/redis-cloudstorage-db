
from cache_db import SingletonRedis
from cloud_storage import SingletonGCS

"""
DBClient
Frontend Key/Value store: Redis
Backend persistent Key/Value Store: Cloud Storage 
"""
class DBClient:

    redis_client = SingletonRedis.get_instance()
    gcs_client = SingletonGCS.get_instance("project_name")

    @classmethod
    def put(cls, key, value):
        """
        Should check if need to handle burst of traffic to update the same key
        Do we need to write the key in a context manager?
        may be need to keep separate functions for atomic, transactional batch opertations, burst requests to update a key
        """
        res = cls.redis_client.put(key, value)

        """
        Should check if need to handle burst of traffic to update the same key
        Do we need to write the key in a context manager?
        may be need to keep separate functions for atomic, transactional batch opertations, burst requests to update a key
        """
        cls.gcs_client.write_to_gcs("project_name", key, value)

    @classmethod
    def get(cls, key):
        # read from redis cache
        value = cls.redis_client.get(key)
        if value:
            return value
        value = cls.gcs_client.get_from_gcs(cls.gcs_client, "project_name", key)
        if value:
            cls.redis_client.put(key, value)
            return value
        return None