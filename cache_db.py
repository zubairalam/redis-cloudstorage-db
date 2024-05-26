import redis
from threading import Lock

class SingletonRedis:
    _instance = None
    _lock = Lock()

    def __init__(self, host='localhost', port=6379, db=0):
        if not SingletonRedis._instance:
            with SingletonRedis._lock:
                if not SingletonRedis._instance:
                    SingletonRedis._instance = redis.Redis(host=host, port=port, db=db)

    @staticmethod
    def get_instance():
        if not SingletonRedis._instance:
            SingletonRedis()
        return SingletonRedis._instance