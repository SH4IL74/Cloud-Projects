# Importing necessary libraries

import csv
import boto3
from datetime import datetime
import re


def lambda_handler(event, context):

    # Intialize the s3 resource
    s3 = boto3.resource('s3', region_name = 'ap-south-1') 

    # Extract the bucket name and csv file name from the event
    message = event['Records'][0]['body']
    match = re.search("for '(.*?)' bucket and file '(.*?)'",message)
    if match:
         bucket_name,csv_file_name = match.groups()
    else:
         print(f"Error parsing message {message}")
    
    # Define the error bucket name
    error_bucket = 'hol-billing-errors-x'
    processed_bucket = 'hol-billing-proccessed-x'

    # Adding Debug lines
    print(f"DEBUG: Attempting to access Bucket: '{bucket_name}'")
    print(f"DEBUG: Attempting to access Key: '{csv_file_name}'")

    # Download the csv file,read the content,decode the content from bytes to strings and split the content into lines
    obj = s3.Object(bucket_name, csv_file_name)
    data = obj.get()['Body'].read().decode('utf-8').splitlines()

    # Intialize the flag (error_found) to false . We will set this flag to true if there is an error
    error_found = False

    # Define valid product lines and valid currencies
    valid_product_lines = ['Bakery','Meat','Dairy']
    valid_currencies = ['USD','MXN','CAD']

    # Read the csv content using csv.reader and iterate through each row . Ignore the header row
    for row in csv.reader(data[1:], delimiter=','):
         # For each line get product line,currency,date and bill amount from specific columns
        date = row[6]
        product_lines = row[4]
        currency  = row[7]
        bill_amount = row[8]

        # Check if the date is valid , If not , set the error flag to true and break the loop
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:  
            error_found = True
            print(f"Error in record {row}: , Invalid date format : {date}")
            break

        # Check if the product line is valid , If not , set the error flag to true and break the loop
        if product_lines not in valid_product_lines:
            error_found = True
            print(f"Error in record {row}: , Invalid product line : {product_lines}")
            break

        # Check if the currency is valid , If not , set the error flag to true and break the loop
        if currency not in valid_currencies:
            error_found = True
            print(f"Error in record {row}: , Invalid currency : {currency}")
            break       

        # Check if the bill amount is negative , If not , set the error flag to true and break the loop
        if float(bill_amount) < 0:
            error_found = True
            print(f"Error in record {row}: , Bill amount cannot be negative : {bill_amount}")
            break

        # After checking all the conditions if there is an error , upload the file to error bucket and break the loop
    if error_found:
        copy_source = {'Bucket': bucket_name, 'Key': csv_file_name}
        try:
                s3.meta.client.copy(copy_source, error_bucket, csv_file_name)
                print(f"File {csv_file_name} has been copied to {error_bucket} due to errors.")
                s3.Object(bucket_name, csv_file_name).delete()
                print(f"File {csv_file_name} has been deleted from {bucket_name}.")
        except Exception as e:
                print(f"Error copying file {csv_file_name} to error bucket: {str(e)}")
        # If there are no errors , print the record
    else:
        copy_source = {'Bucket': bucket_name, 'Key': csv_file_name}
        try:
                s3.meta.client.copy(copy_source, processed_bucket, csv_file_name)
                print(f"File {csv_file_name} has been moved to {processed_bucket} due to errors.")
                s3.Object(bucket_name, csv_file_name).delete()
                print(f"File {csv_file_name} has been deleted from {bucket_name}.")
        except Exception as e:
                print(f"Error copying file {csv_file_name} to error bucket: {str(e)}")
