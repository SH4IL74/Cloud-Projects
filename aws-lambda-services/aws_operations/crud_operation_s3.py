# Importing boto3 library

import boto3

# Specify a boto3 resource and name your bucket


s3 = boto3.resource('s3',region_name='ap-south-1')
bucket_name = 'my-bucket-iiueinjdiuiunqwi'

# Checking if the bucket exists
# Create the bucket if it does not exist

all_my_buckets = [bucket.name for bucket in s3.buckets.all()]
if bucket_name not in all_my_buckets:
    print(f"{bucket_name} is not existing, creating it now...")
    s3.create_bucket(Bucket = bucket_name , CreateBucketConfiguration = {'LocationConstraint': 'ap-south-1'})
    print(f"{bucket_name} has been created successfully.")
else:
    print(f"{bucket_name} already exists.")

# Creating a file and uploading it to the bucket

file_name1 = "file_1.txt"
file_content1 =  "Hello, this is a sample file to be uploaded to S3 bucket using boto3 library in Python."
file_name2 = "file_2.txt"
file_content2 = "This is the second sample file to be uploaded to S3 bucket using boto3 library in Python."
# Uploading the file to the bucket

s3.Bucket(bucket_name).put_object(Key = file_name1 ,Body = file_content1)
s3.Bucket(bucket_name).put_object(Key = file_name2 ,Body = file_content2)
print(f"{file_name1} and {file_name2} have been uploaded to {bucket_name} successfully.")

# Read and print the file from the bucket

obj = s3.Object(bucket_name,file_name1)
body = obj.get()['Body'].read()
print(body)

# Update the file_1 data with new content of file_2 

s3.Object(bucket_name,file_name1).put(Body = file_content2)
obj = s3.Object(bucket_name,file_name1)
body = obj.get()['Body'].read()
print(body)

# Delete the file from the bucket

s3.Object(bucket_name,file_name1).delete()
print(f"{file_name1} has been deleted from {bucket_name} successfully.")
s3.Object(bucket_name,file_name2).delete()
print(f"{file_name2} has been deleted from {bucket_name} successfully")

# Delete the bucket

bucket = s3.Bucket(bucket_name)
bucket.delete()
print(f"{bucket_name} has been deleted successfully.")


