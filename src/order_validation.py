import json
import boto3
import traceback
import os

sqs = boto3.client('sqs')

def lambda_handler(event, context):
    try:
        print(f"Incoming event: {json.dumps(event)}")  # Log the full event for debugging

        # Check if 'body' is present in the event
        if not event.get('body'):
            raise ValueError("Request body is missing")
        
        # Parse the JSON body
        body = json.loads(event['body'])
        print(f"Parsed body: {body}")

        # Validate required fields
        if 'customer_name' not in body or 'items' not in body:
            error_message = f"Invalid payload: {body}"
            print(error_message)
            sqs.send_message(
                QueueUrl=os.environ['DLQ_URL'],
                MessageBody=json.dumps({'error': 'Invalid order', 'order': body}),
                MessageGroupId="dlq-group"  # Required for DLQ FIFO queues
            )
            return {'statusCode': 400, 'body': json.dumps({'message': 'Invalid order'})}
        
        # Send to SQS
        response = sqs.send_message(
            QueueUrl=os.environ['SQS_QUEUE_URL'],
            MessageBody=json.dumps(body),
            MessageGroupId="order-processing-group"  # Required for FIFO queues
        )
        print(f"SQS response: {response}")

        return {'statusCode': 200, 'body': json.dumps({'message': 'Order received'})}
    
    except Exception as e:
        print(f"Unhandled Exception: {e}")
        print("Traceback:", traceback.format_exc())
        return {'statusCode': 500, 'body': json.dumps({'message': 'Internal server error HABACA!!'})}
