#from celery import Celery
import time
import json
import redis
import boto3
import os
import logging

#connect to redis
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
r = redis.StrictRedis.from_url(redis_url)

# Connect to LocalStack (e.g., SQS)
sqs = boto3.client(
    'sqs',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', 'test'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', 'test'),
    region_name=os.getenv('AWS_REGION', 'ap-south-1'),
    endpoint_url="http://sqs.us-east-1.localhost.localstack.cloud:4566"
)

def poll_sqs():
    print("poll sqs called")

    while True:
        response = sqs.receive_message(
        QueueUrl = 'http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/my-queue',
        MaxNumberOfMessages = 10,
        WaitTimeSeconds = 10
        )

        messages = response.get('Messages', [])
        for message in messages:
            sqs_messages = json.loads(message['Body'])
            for sqs_message in sqs_messages:
                #validate data
                if validateData(sqs_message):
                    #process the order
                    if processOrder(sqs_message):
                        print(f'Message processed successfully : {sqs_message["order_id"]}')
                    else:
                        print(f'Failed to process message: {sqs_message["order_id"]}')  
                else:
                    print(f'Data is invalid : {sqs_message["order_id"]}')
                
                sqs.delete_message(QueueUrl = 'http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/my-queue', ReceiptHandle = message['ReceiptHandle'])
        time.sleep(1)    


def processOrder(sqs_message):
    global_stats_filter = "global:stats"
    try:
        ## user stats update
        user_id_filter = f'user_id:{sqs_message["user_id"]}'
        if(r.exists(user_id_filter)):
            r.hset(user_id_filter,'order_count', 1 + int(r.hget(user_id_filter, 'order_count').decode()))
            r.hset(user_id_filter,'total_spend',float(r.hget(user_id_filter, 'total_spend').decode()) + sqs_message['order_value'])
        else:
            r.hset(user_id_filter,'order_count',1)
            r.hset(user_id_filter,'total_spend', sqs_message['order_value'])
        ##global stats update
        if(r.exists(global_stats_filter)):
            r.hset(global_stats_filter,'total_orders',1 + int(r.hget(global_stats_filter, 'total_orders').decode()))
            r.hset(global_stats_filter,'total_revenue', float(r.hget(global_stats_filter, 'total_revenue').decode()) + sqs_message['order_value'])
        else:
            r.hset(global_stats_filter,'total_orders',1)
            r.hset(global_stats_filter,'total_revenue', sqs_message['order_value'])
        return True
    except Exception as ex:
        print(f"Error in processing order : {ex}")
        return False



def validateData(message):
    
    Total_order = 0.0
    ## validate the order_id, user_id and order_value
    if(message['order_id'] == "" or message['user_id'] == ""):
        logging.error(f'either order_id or user_id is null. order_id : {message["order_id"]}, user_id : {message["user_id"]}')
        return False
    elif(type(message['order_value']) not in (int,float)): #validate the order value type
        logging.error(f"order_value not a integer or float value : {message['order_value']}")
        return False
    
    ##validate the order value by using quantity * price
    for i in message['items']:
        Total_order += i["quantity"] * i["price_per_unit"]

    if round(Total_order,2) != message['order_value']:
        logging.error(f' Actual order value : {message["order_value"]} of order_id : {message["order_id"]} is not equal to quantity * price calculated value : {Total_order} ')
        return False
    
    return True

if __name__ == '__main__':       
    poll_sqs()