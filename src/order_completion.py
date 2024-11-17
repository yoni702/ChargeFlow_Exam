import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
eventbridge = boto3.client('events')
table = dynamodb.Table('Orders')

def lambda_handler(event, context):
    for record in event['Records']:
        order = json.loads(record['body'])
        table.update_item(
            Key={'orderId': order['order_id']},
            UpdateExpression='SET status = :s',
            ExpressionAttributeValues={':s': 'COMPLETED'}
        )
        eventbridge.put_events(
            Entries=[
                {
                    'Source': 'order.process',
                    'DetailType': 'OrderCompleted',
                    'Detail': json.dumps(order)
                }
            ]
        )
