import json
import boto3
import os

sns_client = boto3.client('sns')

def lambda_handler(event, context):
    detail = json.loads(event['detail'])
    order_id = detail['orderId']
    status = detail['status']

    # Sujet et message pour la notification
    subject = f"Order {order_id} Status Update"
    message = f"Your order with ID {order_id} has been {status}."

    # Envoyer une notification via SNS
    response = sns_client.publish(
        TopicArn=os.environ['SNS_TOPIC_ARN'],
        Subject=subject,
        Message=message
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Notification sent successfully'})
    }