import os
import boto3


# create s3 bucket
def create_s3_bucket(acl, bucket_name, region):
    s3client = boto3.client('s3',
                            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                            region_name=os.environ['AWS_AZ'])
    if acl is None:
        acl = 'private'
    try:
        if region in ('us-east-1', None):
            s3client.create_bucket(ACL=acl, Bucket=bucket_name)
        else:
            s3client.create_bucket(ACL=acl, Bucket=bucket_name,
                                   CreateBucketConfiguration={
                                       'LocationConstraint': region})
        print('bucket created: ', bucket_name)
    except Exception as error:
        print(error)


# list s3 bucket
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


# upload file
# if bucket does't exits, create it and then upload
def upload_s3_file(filename, bucket_name, key, acl='public-read'):
    if key is None:
        key = filename.split('/')[-1]
    s3client = boto3.client('s3',
                            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                            region_name=os.environ['AWS_AZ'])
    try:
        if not bucket_exists(bucket_name):
            create_s3_bucket(acl, bucket_name, None)
        s3client.upload_file(filename, bucket_name, key,
                             ExtraArgs={
                                 'ACL': acl})
        print('File uploaded')
    except Exception as error:
        print(error)

    location = s3client.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
    if location is None:
        url = "https://%s.s3.amazonaws.com/%s" % (bucket_name, key)
    else:
        url = "https://%s.s3.%s.amazonaws.com/%s" % (bucket_name, location, key)

    print(url)


# check if bucket already exists
def bucket_exists(bucket_name):
    s3 = boto3.resource('s3')
    return s3.Bucket(bucket_name).creation_date is not None
