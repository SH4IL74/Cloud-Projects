# Required libraries
import boto3
import io
import csv
import logging

# Constants - database and credential details, and currency conversion rates
currency_conversion_to_usd = {'USD':1,'CAD':0.79,'MXN':0.05}

# Constants - database and credential details, and currency conversion rates
# Boto3 clients for Aws services
s3_client = boto3.client('s3',region_name = 'ap-south-1')

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Function to process each record/row from the CSV file
def process_record(record):
    id,company_name,country,city,product_line,item,bill_date,currency,bill_amount = record
    bill_amount = float(bill_amount)

    # Convert the bill amount to USD using conversion rates
    rate = currency_conversion_to_usd.get(currency)
    if rate:
        usd_amount = bill_amount*rate
    else:
        logger.info(f"No rate found for currency:{currency}")
    print(f"Id:{id}: currency:{currency} rate:{rate}")


def lambda_handler(event,context):
    try:
        # Get the bucket name and file name from the event
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        s3_file = event['Records'][0]['s3']['object']['key']

        # Read the file from s3
        response = s3_client.get_object(Bucket = bucket_name,Key = s3_file)
        data = response['Body'].read().decode('utf-8')

        # Use csv reader to process the CSV data
        csv_reader = csv.reader(io.StringIO(data))
        next(csv_reader)

        # Process each record in the CSV file
        for record in csv_reader:
            process_record(record)
        
        logger.info("Lambda has finished execution")

    except Exception as e:
        # If an unexpected error  occurs, log an error message
        logger.error(f"ERROR: unexpected error :{e}")