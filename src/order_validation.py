import json
import boto3
import traceback
import os

sqs = boto3.client('sqs')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        if 'customer_name' not in body or 'items' not in body:
            sqs.send_message(
                QueueUrl=os.environ['DLQ_URL'],
                MessageBody=json.dumps({'error': 'Invalid order', 'order': body})
            )
            return {'statusCode': 400, 'body': json.dumps({'message': 'Invalid order'})}
        
        sqs.send_message(
            QueueUrl=os.environ['SQS_QUEUE_URL'],
            MessageBody=json.dumps(body)
        )
        return {'statusCode': 200, 'body': json.dumps({'message': 'Order received'})}
    except Exception as e:
        print(f"Error: {e}")
        print("Traceback:", traceback.format_exc())

        return {'statusCode': 500, 'body': json.dumps({'message': 'Internal server AhAH error'})}
