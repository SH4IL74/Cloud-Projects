# Importing required libraries 
import boto3
import io
import csv
import logging

# Constants - database and credential details, and currency conversion rates 
currency_conversion_to_usd = {'USD':1,'CAD':0.79,'MXN':0.05}

# Boto3 clients for AWS services 
LOCALSTACK_ENDPOINT = "http://localhost:4566"
s3 = boto3.client(
    's3',
    region_name = 'ap-south-1',
    endpoint_url = LOCALSTACK_ENDPOINT,
    aws_access_key_id = "test",
    aws_secret_access_key = "test"
    )

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Function to process each row from the CSV file
def process_record(record):
    # 1. First, check if the row is valid before doing anything
    if not record or len(record) < 9:
        return 

    try:
        # 2. Unpack the data once
        (id, company_name, country, city, product_line, 
         item, bill_date, currency, bill_amount) = record
        
        # 3. Convert to float immediately
        bill_amount = float(bill_amount)

        # 4. Perform the conversion logic
        rate = currency_conversion_to_usd.get(currency)
        
        if rate:
            usd_amount = bill_amount * rate
            print(f" ID:{id} | {bill_amount} {currency} -> {usd_amount:.2f} USD")
        else:
            logger.info(f"No rate found for currency: {currency}")
            print(f" Id:{id}: No rate found for {currency}")

    except ValueError as e:
        print(f" Skipping malformed row or bad number: {record} | Error: {e}")
    except Exception as e:
        print(f" Unexpected error in row: {e}")

def lambda_handler(event,context):
    try:
        print("1. Extracting bucket and file name...")
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        s3_file = event['Records'][0]['s3']['object']['key']
        print(f"Target: bucket={bucket_name}, file={s3_file}")

        print("2. Attempting to contact S3...")
        response = s3.get_object(Bucket=bucket_name, Key=s3_file)
        
        print("3. Reading data...")
        data = response['Body'].read().decode('utf-8')
        
        print(f"4. Data loaded! First 50 chars: {data[:50]}")

        # Use the csv reader to process the CSV data
        csv_reader = csv.reader(io.StringIO(data))
        try:
            next(csv_reader) # Skip Header
        except StopIteration:
            print("File is empty!")
            return

        for record in csv_reader:
            process_record(record)
    
    except Exception as e:
        print(f" ERROR:{e}")
        # If an unexpected error occues log an error message
        logger.error(f"ERROR: unexpected error: {e}")

if __name__ == "__main__":
    # Create a mock event to test the function manually
    test_event = {
        "Records": [{
            "s3": {
                "bucket": {"name": "my-billing-bucket"},
                "object": {"key": "billing_data_meat_june_2023.csv"}
            }
        }]
    }
    print("Manual test starting...")
    lambda_handler(test_event, None)