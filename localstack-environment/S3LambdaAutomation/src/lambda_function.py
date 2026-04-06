import csv
import boto3
from datetime import datetime

# LOCALSTACK_ENDPOINT = "http://localhost:4566" # Use this if running script from host
LOCALSTACK_ENDPOINT = "http://host.docker.internal:4566" 

def lambda_handler(event, context):
    # Initialize with LocalStack endpoint
    s3 = boto3.resource('s3', endpoint_url=LOCALSTACK_ENDPOINT, region_name='ap-south-1') 

    bucket_name = event['Records'][0]['s3']['bucket']['name']
    csv_file_name = event['Records'][0]['s3']['object']['key']
    
    error_bucket = 'hol-billing-errors-x'
    processed_bucket = 'hol-billing-proccessed-x'

    print(f"DEBUG: Processing file {csv_file_name} from {bucket_name}")

    try:
        obj = s3.Object(bucket_name, csv_file_name)
        data = obj.get()['Body'].read().decode('utf-8').splitlines()
        
        error_found = False
        valid_product_lines = ['Bakery','Meat','Dairy']
        valid_currencies = ['USD','MXN','CAD']

        # Skip header and validate
        reader = csv.reader(data)
        header = next(reader) # Skip header row

        for row in reader:
            if not row: continue # Skip empty lines
            
            # Adjust indices based on your specific CSV structure
            product_line = row[4]
            date_val = row[6]
            currency = row[7]
            bill_amount = row[8]

            # Validation logic
            try:
                datetime.strptime(date_val, '%Y-%m-%d')
                if product_line not in valid_product_lines or \
                   currency not in valid_currencies or \
                   float(bill_amount) < 0:
                    error_found = True
                    break
            except (ValueError, IndexError):
                error_found = True
                break

        # Move file based on validation result
        target_bucket = error_bucket if error_found else processed_bucket
        copy_source = {'Bucket': bucket_name, 'Key': csv_file_name}
        
        s3.meta.client.copy(copy_source, target_bucket, csv_file_name)
        s3.Object(bucket_name, csv_file_name).delete()
        
        print(f"File moved to: {target_bucket}")

    except Exception as e:
        print(f"System Error: {str(e)}")
        return {"status": "error", "message": str(e)}

    return {"status": "success", "validated": not error_found}