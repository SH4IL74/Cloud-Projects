# Importing the boto3 library
import boto3

# Specify a boto3 resource and name the bucket 
Localstack_endpoint = "http://localhost:4566" 
my_bucket = "my-s3-bucket"
Region = "ap-south-1"
s3 = boto3.resource(
    's3',
    aws_access_key_id  = "test",
    aws_secret_access_key = "test",
    endpoint_url = Localstack_endpoint,
    region_name = Region
)

# Checking if the bucket already exists
# If not , creating a new bucket
all_my_buckets = [bucket.name for bucket in s3.buckets.all() ]
if my_bucket not in all_my_buckets:
    print(f"The bucket does not exist. Creating a new bucket with name {my_bucket} ")
    s3.create_bucket(Bucket = my_bucket,CreateBucketConfiguration = {'LocationConstraint':'ap-south-1'})
    print(f"The bucket with name {my_bucket} created successfully")
else:
    print(f"The bucket with name already exists")

# Creating files to insert in the bucket 
file_name_1 = "file_1.txt"
file_content_1 = "This is the first sample file to insert in the bucket using botos and in the localstack environment"
file_name_2 = "file_2.txt"
file_content_2 = "This is the second sample file to insert in the bucket using botos and in the localstack environment"

# Inserting the files inside the bucket 
s3.Bucket(my_bucket).put_object(Key = file_name_1 , Body = file_content_1)
s3.Bucket(my_bucket).put_object(Key = file_name_2 , Body = file_content_2)
print(f"Inserting the files {file_name_1} and {file_name_2} in the bucket {my_bucket} successfully")

# Read and print the file from the bucket
obj = s3.Object(my_bucket,file_name_1)
body = obj.get()['Body'].read()
print(body)

# Update the file from file 1 to file 2
s3.Object(my_bucket,file_name_1).put(Body = file_content_2)
obj = s3.Object(my_bucket,file_name_1)
body = obj.get()['Body'].read()
print(body)

# Deleting the files from the bucket 
s3.Object(my_bucket,file_name_1).delete()
print(f"The file with name {file_name_1} is deleted successfully from bucket {my_bucket}")
s3.Object(my_bucket,file_name_2).delete()
print(f"The file with name {file_name_2} is deleted successfully from bucket {my_bucket}")

# Deleting th bucket
bucket = s3.Bucket(my_bucket)
bucket.delete()
print(f"Bucket with name {my_bucket} deleted successfully")