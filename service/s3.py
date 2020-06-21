import os
import boto3


def list_s3_buckets():
    s3client = boto3.client('s3',
                            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                            region_name=os.environ['AWS_AZ'])
    buckets = s3client.list_buckets()
    bucket_names = []
    for bucket in buckets['Buckets']:
        # print("Bucket Name --> {} Created Date {}", format(bucket['Name'], str(bucket['CreationDate'])))
        bucket_names.append(bucket['Name'])
    return bucket_names


# upload file, directory to a bucket
# if bucket does't exits, create it and then upload
def upload_s3_file(filename, bucket_name, key=None):
    if key is None:
        key = filename.split('/')[-1]

    s3client = boto3.client('s3',
                            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                            region_name=os.environ['AWS_AZ'])
    try:
        if not bucket_exists(bucket_name):
            s3client.create_bucket(Bucket=bucket_name)
        s3client.upload_file(filename, bucket_name, key)
        print('File uploaded')
    except Exception as error:
        print(error)


# check if bucket already exists 
def bucket_exists(bucket_name):
    s3 = boto3.resource('s3')
    return s3.Bucket(bucket_name).creation_date is not None


# upload_s3_file('/tmp/newfile.txt', 'test-cli-jay-bucket', None)
list_bucket = list_s3_buckets()
print(list_bucket)
