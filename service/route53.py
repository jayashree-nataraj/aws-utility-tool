import boto3
import os
import uuid


def get_all_hosted_zones():
    route53client=boto3.client('route53',
                               aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                               aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                               region_name=os.environ['AWS_AZ'])
    response = route53client.list_hosted_zones()
    hostedzones = response['HostedZones']
    hosted_zones = []
    hosted_zone_list = []
    for hostedzone in hostedzones:
        hosted_zones.append(hostedzone['Name'])
        hosted_zones.append(hostedzone['Id'].split('/')[-1])
        hosted_zones.append(hostedzone['ResourceRecordSetCount'])
        hosted_zone_list.append(hosted_zones)
        hosted_zones = []

    return hosted_zone_list


def get_all_hosted_zones_count():
    route53client=boto3.client('route53',
                               aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                               aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                               region_name=os.environ['AWS_AZ'])
    response = route53client.get_hosted_zone_count()
    hosted_zone_count = response['HostedZoneCount']

    return hosted_zone_count


def list_resource_record_sets(hostedzoneid, maxitems):
    route53client=boto3.client('route53',
                               aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                               aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                               region_name=os.environ['AWS_AZ'])

    response = route53client.list_resource_record_sets(HostedZoneId=hostedzoneid, MaxItems=maxitems)
    recordsets = response['ResourceRecordSets']

    record_sets = []
    recors_set_list = []
    for recordset in recordsets:
        record_sets.append(recordset['Name'])
        record_sets.append(recordset['Type'])
        record_sets.append(recordset['TTL'])
        record_sets.append(recordset['ResourceRecords'])
        recors_set_list.append(record_sets)
        record_sets = []

    return recors_set_list


def create_hosted_zone(name, comment, vpc_region, vpcid, private_zone=False):
    call_reference=str(uuid.uuid4())
    if comment is None:
        comment = "this is a new hosted zone"
    hostedzoneconfig = {
        'Comment': comment,
        'PrivateZone': private_zone
    }
    if private_zone:
        if vpc_region is None or vpcid is None:
            vpc_region = 'us-east-1'
            vpcid = 'vpc-2f763f55'
        vpc = {
            'VPCRegion': vpc_region,
            'VPCId' : vpcid
        }

    route53client=boto3.client('route53',
                               aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                               aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                               region_name=os.environ['AWS_AZ'])
    response = route53client.create_hosted_zone(Name=name, HostedZoneConfig=hostedzoneconfig, CallerReference=call_reference, VPC=vpc)
    print(response)


def delete_hosted_zone(hostedzoneid):
    route53client=boto3.client('route53',
                               aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                               aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                               region_name=os.environ['AWS_AZ'])
    try:
        response = route53client.delete_hosted_zone(Id=hostedzoneid)
        status = response['ResponseMetadata']['HTTPStatusCode']
        print('Status is: ', status)
    except Exception as error:
        print(error)


# count = get_all_hosted_zones_count()
# print(count)

# get_list_route = get_all_hosted_zones()
# print(get_list_route)

# get_list_records = list_resource_record_sets('Z0082379324UOUCAU9VNP', '10')
# print(get_list_records)

# create_hosted_zone('bangaloreprivate.com', None, None, None, True)
# delete_hosted_zone('Z01008541J5LQCNMR06VU')