import json, boto3, os, csv

def lambda_handler(event, context):
    # THE OVERRIDE: Using the internal LocalStack DNS
    endpoint = "http://localhost.localstack.cloud:4566"
    
    s3 = boto3.client('s3', endpoint_url=endpoint)
    sns = boto3.client('sns', endpoint_url=endpoint)
    ses = boto3.client('ses', endpoint_url=endpoint)

    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        # S3 Process
        s3.get_object(Bucket=bucket, Key=key)
        
        # SNS Alert
        sns.publish(
            TopicArn='arn:aws:sns:ap-south-1:000000000000:TaxesAPIConnectionError',
            Message=f"Manual Override Success: Processed {key}",
            Subject="Pipeline Update"
        )

        # Move File
        s3.copy_object(Bucket="my-processed-bucket", CopySource={'Bucket': bucket, 'Key': key}, Key=key)
        s3.delete_object(Bucket=bucket, Key=key)

        # SES Email
        ses.send_email(
            Source='shail@example.com',
            Destination={'ToAddresses': ['shail@example.com']},
            Message={'Subject': {'Data': 'Success'}, 'Body': {'Text': {'Data': 'File moved.'}}}
        )
        return {"statusCode": 200, "body": "Success"}
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}
