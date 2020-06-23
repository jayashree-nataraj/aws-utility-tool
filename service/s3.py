import os
import boto3
import argparse


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
def upload_s3_file(filepath, bucket_name, key, acl='public-read'):
    if key is None:
        key = filepath.split('/')[-1]
    s3client = boto3.client('s3',
                            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                            region_name=os.environ['AWS_AZ'])
    try:
        if not bucket_exists(bucket_name):
            create_s3_bucket(acl, bucket_name, None)
        s3client.upload_file(filepath, bucket_name, key,
                             ExtraArgs={
                                 'ACL': acl})
        print('File uploaded', key)
        location = s3client.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
        if location is None:
            url = "https://%s.s3.amazonaws.com/%s" % (bucket_name, key)
        else:
            url = "https://%s.s3.%s.amazonaws.com/%s" % (bucket_name, location, key)

        print('File URL: ', url)
    except Exception as error:
        print(error)


# check if bucket already exists
def bucket_exists(bucket_name):
    s3 = boto3.resource('s3')
    return s3.Bucket(bucket_name).creation_date is not None


# Create arg parser and subparsers
parser = argparse.ArgumentParser(description='Run s3 commands')

# add arguments
parser.add_argument('--action', choices=['list', 'create_bucket', 'upload_file'], help="allowed actions")
parser.add_argument('--acl', default="public-read", help='acl for the bucket')
parser.add_argument('--bucket', help="bucket name")
parser.add_argument('--region', default="us-east-1", help="region")
parser.add_argument('--filepath', help="full path of the file")
parser.add_argument('--key', help="file name to be set after upload")

# process arguments
args = vars(parser.parse_args())

if args['action'] is None:
    print('--action is a mandatory argument. You cannot use this utility without --action argument')
    exit(1)


if args['action'] == 'list': # 'list' action
    print(list_s3_buckets())

elif args['action'] == 'create_bucket': # 'create_bucket' action
    if args['bucket'] is None:
        print('--bucket is a mandatory argument for create_bucket action')
        print('--region and --acl are optional arguments for create_bucket action')
        print('Example command for create_bucket: --action create_bucket --acl ACL --bucket BUCKET_NAME --region REGION')
    else:
        create_s3_bucket(args['acl'], args['bucket'], args['region'])

elif args['action'] == 'upload_file': # 'upload_file' action
    if args['filepath'] is None or args['bucket'] is None:
        print('--bucket and --filepath are mandatory arguments for upload_file action')
        print('--key and --acl are optional arguments for upload_file action')
        print('Example command for upload_file: --action upload_file --filpath FILEPATH --bucket BUCKET_NAME --region REGION --acl ACL')
    else:
        upload_s3_file(args['filepath'], args['bucket'], args['key'], args['acl'])
