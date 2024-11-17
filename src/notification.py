import json
import boto3
import os

sns = boto3.client('sns')

def lambda_handler(event, context):
    for record in event['Records']:
        order = json.loads(record['body'])
        message = f"Order {order['order_id']} is completed."
        sns.publish(
            TopicArn=os.environ['NOTIFICATION_TOPIC'],
            Message=message
        )
