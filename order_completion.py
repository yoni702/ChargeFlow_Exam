import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
event_client = boto3.client('events')

# DynamoDB table
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def lambda_handler(event, context):
    detail = json.loads(event['detail'])
    order_id = detail['orderId']

    # Mettre à jour le statut de la commande à "COMPLETED"
    table.update_item(
        Key={'orderId': order_id},
        UpdateExpression='SET orderStatus = :status',
        ExpressionAttributeValues={':status': 'COMPLETED'}
    )

    # Émettre un événement de succès à EventBridge
    event_client.put_events(
        Entries=[
            {
                'Source': 'order.completion',
                'DetailType': 'OrderCompleted',
                'Detail': json.dumps({'orderId': order_id, 'status': 'COMPLETED'}),
                'EventBusName': os.environ['EVENT_BUS_NAME']
            }
        ]
    )

    return {'statusCode': 200}