from fastapi import FastAPI
import redis
import uvicorn
import os

api = FastAPI()

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
r = redis.StrictRedis.from_url(redis_url)

@api.get('/users/{user_id}/stats')
def userStats(user_id):
    if(r.exists(f'user_id:{user_id}')):
        return {"user_id" : user_id,
                "order_count" : r.hget(f'user_id:{user_id}','order_count'),
                "total_spend" : r.hget(f'user_id:{user_id}','total_spend')}
    else:
        return {"message": "User Id Does Not Exist"}

@api.get('/stats/global')
def globalStats():
    return {"total_orders" : r.hget("global:stats",'total_orders'),
            "total_revenue" : r.hget("global:stats",'total_revenue')}

@api.get("/")
def read_root():
    return {"message": "Hello, Qyrus !!"}


if __name__ == '__main__':
    # Run FastAPI app on a specific port (e.g., port 8001)
    uvicorn.run(api, host="0.0.0.0", port=8080)

