# ChargeFlow_Exam
Exam

![[Exam.png]]
---
## Local Development

### Installing Sam 
    brew install aws-sam-cli
    sam --version
    aws configure

### python Special dependencies 
    pip3 install boto3

### Configure Github Secrets
        - AWS_ACCESS_KEY_ID 
        - AWS_SECRET_ACCESS_KEY 
        - EVENT_BUS_NAME
        - DYNAMODB_TABLE_NAME
        - SQS_QUEUE_NAME
        - SNS_TOPIC_NAME


### Check the exercise
    
curl -X POST https://s1c48wo1df.execute-api.us-east-1.amazonaws.com/prod/order \
-H "Content-Type: application/json" \
-d '{
    "customer_name": "John Doe",
    "items": [
        {"item_id": "item1", "quantity": 2},
        {"item_id": "item2", "quantity": 1}
    ]
    }'


### Check the exercise From Postman
https://s1c48wo1df.execute-api.us-east-1.amazonaws.com/prod/order

    {
    "customer_name": "John Doe",
    "items": [
        {"item_id": "item1", "quantity": 2},
        {"item_id": "item2", "quantity": 1}
    ]
    }


## Technical Debt

Multi Repository 
- Step 1 Separate Lambda from Iac 
- Ci Cd For IaC only  
- Ci Cd For Lambdas 