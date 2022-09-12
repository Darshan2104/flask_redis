from redis import Redis


def hello_redis():
    try:

        key1 = "Name"
        val1 = 5

        redis = Redis()
        redis.flushall()
        # redis.set("Name", "Darshan")
        redis.set(key1, val1)
        msg = redis.get(key1)
        print(f"Key 1 :{msg}")
        # print(type(msg))

        # redis.set(key1, 'updated_'+msg.decode('UTF-8'))
        # updated_msg = redis.get("Name")
        # print(updated_msg)
        # ///............................
        key2 = "Nums"
        val2 = [1, 2, 3]

        for x in val2:
            redis.rpush(key2, x)
        ans = redis.lrange(key2, 0, -1)
        print(f"Key 2 :{ans}")

        l = len(ans)
        for x in range(l):
            # pop from the right and push updated to left
            temp = (redis.lpop(key2))
            redis.rpush(key2, 'updated_'+temp.decode('UTF-8'))
        updated_ans = redis.lrange(key2, 0, -1)
        print(updated_ans)

    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    hello_redis()
