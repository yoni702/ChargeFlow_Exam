import json
import boto3
import os

sqs_client = boto3.client('sqs')

def lambda_handler(event, context):
    detail = json.loads(event['detail'])
    if 'customerName' in detail and 'items' in detail:
        sqs_client.send_message(
            QueueUrl=os.environ['SQS_QUEUE_URL'],
            MessageBody=json.dumps(detail)
        )
    else:
        print("Invalid order:", detail)