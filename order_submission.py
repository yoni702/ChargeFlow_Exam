import json
import boto3

import os

event_client = boto3.client('events')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    response = event_client.put_events(
        Entries=[
            {
                'Source': 'order.submission',
                'DetailType': 'OrderSubmitted',
                'Detail': json.dumps(body),
                'EventBusName': os.environ['EVENT_BUS_NAME']
            }
        ]
    )
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Order submitted successfully!'})
    }