import json
import boto3
import os

sqs = boto3.client('sqs')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    if 'customer_name' not in body or 'items' not in body:
        sqs.send_message(
            QueueUrl=os.environ['DLQ_URL'],
            MessageBody=json.dumps({'error': 'Invalid order', 'order': body})
        )
        return {'statusCode': 400, 'body': 'Invalid order'}
    
    sqs.send_message(
        QueueUrl=os.environ['SQS_QUEUE_URL'],
        MessageBody=json.dumps(body)
    )
    return {'statusCode': 200, 'body': 'Order received'}
