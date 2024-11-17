import json
import boto3
import traceback
import os

sqs = boto3.client('sqs')

def lambda_handler(event, context):
    try:
        print(f"Incoming event: {json.dumps(event)}")  # Log the entire event for debugging

        # Check if 'body' is present in the event
        if not event.get('body'):
            raise ValueError("Request body is missing")
        
        # Parse the JSON body from the event
        body = json.loads(event['body'])
        print(f"Parsed body: {body}")

        # Validate required fields
        if 'customer_name' not in body or 'items' not in body:
            sqs.send_message(
                QueueUrl=os.environ['DLQ_URL'],
                MessageBody=json.dumps({'error': 'Invalid order', 'order': body})
            )
            return {'statusCode': 400, 'body': json.dumps({'message': 'Invalid order'})}
        
        # Send the valid order to the SQS queue
        sqs.send_message(
            QueueUrl=os.environ['SQS_QUEUE_URL'],
            MessageBody=json.dumps(body)
        )
        return {'statusCode': 200, 'body': json.dumps({'message': 'Order received'})}
    
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Traceback:", traceback.format_exc())
        return {'statusCode': 500, 'body': json.dumps({'message': 'Internal server error HaHa3'})}
