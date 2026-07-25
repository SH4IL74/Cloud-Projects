import json
import boto3
import os

# Dynamically route to LocalStack's internal host
host = os.environ.get('LOCALSTACK_HOSTNAME', 'localhost.localstack.cloud')
endpoint_url = f"http://{host}:4566"

dynamodb = boto3.resource(
    'dynamodb', 
    endpoint_url=endpoint_url, 
    region_name="ap-south-1"
)
table = dynamodb.Table('visitor_count')

def lambda_handler(event, context):
    try:
        response = table.update_item(
            Key={'id': 'visitors'},
            UpdateExpression='ADD quantity :inc',
            ExpressionAttributeValues={':inc': 1},
            ReturnValues='UPDATED_NEW'
        )
        
        views = response['Attributes']['quantity']
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'views': int(views)})
        }
    except Exception as e:
        print(f"Error connecting to DynamoDB: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }