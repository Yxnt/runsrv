import redis


class Redis(object):
    """连接Redis"""
    def __init__(self, ip, port, db, password):
        self.ip = ip
        self.port = port
        self.db = db
        self.password = password

    def __set_connect(self):
        pool = redis.ConnectionPool(
            host=self.ip,
            port=self.port,
            db=self.db,
            password=self.password
        )
        return redis.Redis(connection_pool=pool)

    def __r(self):
        return self.__set_connect()

    def get(self, key):
        return self.__r().get(key)

    def set(self, key, value, time):
        return self.__r().set(key, value, ex=time, nx=True)

    def hset(self, name, key, value):
        return self.__r().hset(name, key, value)

    def hget(self, name, key):
        return self.__r().hget(name, key)


if __name__ == '__main__':
    r = redis_cli()

    print(r.ip)
