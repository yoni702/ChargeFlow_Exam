import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
event_client = boto3.client('events')

# DynamoDB table
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def lambda_handler(event, context):
    for record in event['Records']:
        order = json.loads(record['body'])
        order_id = order['orderId']
        items = order['items']

        # Simuler la vérification d'inventaire (ici, on suppose que tous les articles sont en stock)
        inventory_available = True

        if inventory_available:
            # Mettre à jour le statut de la commande dans DynamoDB
            table.update_item(
                Key={'orderId': order_id},
                UpdateExpression='SET orderStatus = :status',
                ExpressionAttributeValues={':status': 'IN_PROCESS'}
            )

            # Émettre un événement de succès à EventBridge
            event_client.put_events(
                Entries=[
                    {
                        'Source': 'order.inventory',
                        'DetailType': 'InventoryChecked',
                        'Detail': json.dumps({'orderId': order_id, 'status': 'IN_PROCESS'}),
                        'EventBusName': os.environ['EVENT_BUS_NAME']
                    }
                ]
            )
        else:
            # Émettre un événement d'échec à EventBridge si l'inventaire est insuffisant
            event_client.put_events(
                Entries=[
                    {
                        'Source': 'order.inventory',
                        'DetailType': 'InventoryFailed',
                        'Detail': json.dumps({'orderId': order_id, 'status': 'FAILED'}),
                        'EventBusName': os.environ['EVENT_BUS_NAME']
                    }
                ]
            )

    return {'statusCode': 200}