import boto3
import json
import os

# Connect to LocalStack (e.g., SQS)
sqs = boto3.client(
    'sqs',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', 'test'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', 'test'),
    region_name=os.getenv('AWS_REGION', 'ap-south-1'),
    endpoint_url="http://sqs.us-east-1.localhost.localstack.cloud:4566"
)

def sampleMessage():
        return json.dumps([{
            "order_id": "ORDER1",
            "user_id": "USER1",
            "order_timestamp": "2024-12-13T10:00:00Z",
            "order_value": 99.99,
            "items": [
            { "product_id": "P001", "quantity": 2, "price_per_unit": 20.00 },
            { "product_id": "P002", "quantity": 1, "price_per_unit": 59.99 }
            ],
            "shipping_address": "123 Main St, Springfield",
            "payment_method": "CreditCard"
            }
            ,{
            "order_id": "ORDER2",
            "user_id": "USER2",
            "order_timestamp": "2024-12-13T10:00:00Z",
            "order_value": 200.00,
            "items": [
            { "product_id": "P003", "quantity": 1, "price_per_unit": 120.00 },
            { "product_id": "P004", "quantity": 1, "price_per_unit": 80.00 }
            ],
            "shipping_address": "123 Main St, AutumnField",
            "payment_method": "Cash"
            }
            ,{
            "order_id": "ORDER3",
            "user_id": "USER3",
            "order_timestamp": "2024-12-13T10:00:00Z",
            "order_value": 140.00,
            "items": [
            { "product_id": "P005", "quantity": 2, "price_per_unit": 40.00 },
            { "product_id": "P006", "quantity": 1, "price_per_unit": 60.00 }
            ],
            "shipping_address": "123 Main St, Winterfell",
            "payment_method": "DebitCard"
            }
            ,{
            "order_id": "ORDER4",
            "user_id": "USER2",
            "order_timestamp": "2024-12-13T10:00:00Z",
            "order_value": 159.99,
            "items": [
            { "product_id": "P001", "quantity": 5, "price_per_unit": 20.00 },
            { "product_id": "P002", "quantity": 1, "price_per_unit": 59.99 }
            ],
            "shipping_address": "123 Main St, Springfield",
            "payment_method": "CreditCard"
            }
            #Error Record
            ,{
            "order_id": "ORDER5",
            "user_id": "",
            "order_timestamp": "2024-12-13T10:00:00Z",
            "order_value": 180.00,
            "items": [
            { "product_id": "P008", "quantity": 4, "price_per_unit": 25.00 },
            { "product_id": "P009", "quantity": 1, "price_per_unit": 80.00 }
            ],
            "shipping_address": "123 Main St, Nashville",
            "payment_method": "Cash"
            }
            #Error Record
            ,{
            "order_id": "ORDER6",
            "user_id": "USER2",
            "order_timestamp": "2024-12-13T10:00:00Z",
            "order_value": 500,
            "items": [
            { "product_id": "P012", "quantity": 2, "price_per_unit": 300.00 },
            { "product_id": "P011", "quantity": 1, "price_per_unit": 200.00 }
            ],
            "shipping_address": "123 Main St, King's Landing",
            "payment_method": "Cash"
            }]
            )

# Send a message to the SQS queue

def send_sqs_message(message):
    print("send_sqs_message_called")
    ##sqs.create_queue(QueueName='my-queue')
    queue_url = 'http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/my-queue'
    sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message
        )
send_sqs_message(sampleMessage())
