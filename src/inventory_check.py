import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Orders')

def lambda_handler(event, context):
    for record in event['Records']:
        order = json.loads(record['body'])
        inventory_available = True  # Simulate inventory check
        status = 'IN_PROCESS' if inventory_available else 'FAILED'
        table.put_item(Item={'orderId': order['order_id'], 'status': status})
