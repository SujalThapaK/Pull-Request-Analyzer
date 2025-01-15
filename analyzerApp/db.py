from redis import Redis

redis_client = Redis(host="redis", port=6379, db=0)

def store_result(task_id, result):
    redis_client.set(task_id, result)

def get_task_result(task_id):
    result = redis_client.get(task_id)
    return result.decode("utf-8") if result else None