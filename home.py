from itertools import count
import json
from flask import Flask, Response, request
import pymongo
# from bson.objectid import ObjectId
from redis import Redis

#################################################################
app = Flask(__name__)
# redis = Redis(host='redis', port=6379)
redis = Redis()  # default localhost:6379

######################## DB connection ###########################

try:

    m = "mongodb+srv://darshan:X85fQwZNGeqYkZOu@cluster0.xnd1g0k.mongodb.net/?retryWrites=true&w=majority"
    # mongo = pymongo.MongoClient(
    #     host="localhost",
    #     port=27017,
    #     serverSelectionTimeoutMS=1000
    # )
    mongo = pymongo.MongoClient(m)
    db = mongo.company
    print(db.list_collection_names())
    # mongo.server_info()  # trigger exception if can't connect to db
except:
    print("Error- cannot connect to db")


######################## redis ###########################

# @app.route("/hello", methods=["GET"])
# def hello():
#     try:
#         redis.set("Name", "Darshan")
#         print(redis.get("Name"))

#     .........For more operation follow : check_redis.py .........

#     except Exception as ex:
#         print(ex)

######################## Read ###########################

@app.route("/users", methods=["GET"])
def get_some_users():
    try:
        redis.flushall()
        data = list(db.users.find())
        key1 = "name"
        key2 = "lastname"
        # create list and push elements into the right side of the list

        count = 0
        for entry in data:
            redis.rpush(key1, entry[key1])
            redis.rpush(key2, entry[key2])
            count += 1
        # After above for loop: name = ["A","B","C"]
        #                       lastname = ["AA","BB,"CC"]

        # update name and last name
        for _ in range(count):
            # temp1 = (redis.lpop(key1))
            # redis.set("temp",temp1)
            # redis.rpush(key1, 'updated_'+temp1.decode('UTF-8'))
            redis.set("temp1", redis.lpop(key1))
            redis.rpush(key1, 'updated_' + redis.get("temp1").decode('UTF-8'))

            temp2 = (redis.lpop(key2))
            redis.rpush(key2, 'updated_'+temp2.decode('UTF-8'))

        # After above for loop: name = ["updated_A","updated_B","updated_C"]
        #                       lastname = ["updated_AA","updated_BB,"updated_CC"]

        # clear the redis cache and store that updated data to new collection- updated_users

        for _ in range(count):
            updated_user = {key1: redis.lpop(key1), key2: redis.lpop(key2)}
            db.updated_users.insert_one(updated_user)

        # for user in data:
        #     user["_id"] = str(user["_id"])
        # print(data)
        return Response(
            response=json.dumps(data),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({
                "message": "Can't read Users"
            }),
            status=500,
            mimetype="application/json"
        )


########################
if __name__ == "__main__":
    app.run(port=8090, debug=True)
