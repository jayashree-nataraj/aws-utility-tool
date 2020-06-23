import boto3
import os
import uuid
import argparse


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
    if maxitems is None:
        maxitems = '20'
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


# Create arg parser and subparsers
parser = argparse.ArgumentParser(description='Run route53 commands')

# add all arguments
parser.add_argument('--action', choices=['list_hostedzones', 'list_recordsets', 'create', 'delete'], help="allowed actions")
parser.add_argument('--hostedzone-id', help='hostedzone-id is required argument to list hosted zone, delete hosted zone')
parser.add_argument('--zone-name', help="zone-name is a required argument to create hosted zone ")
parser.add_argument('--region', default="us-east-1", help="aws region")
parser.add_argument('--comment', help="Include comment to enter details about the hosted zone")
parser.add_argument('--vpc-region', help="Required argument to create provate hosted zone")
parser.add_argument('--vpcid', help="Required argument for the selected --vpc-region")
parser.add_argument('--private_zone', help="if True, the hosted zones are created in VPC network. if True --vpc-region, --vpcid are required arguments ")
parser.add_argument('--maxitems', help="Number if hosted zones items you want to display")


# process arguments
args = vars(parser.parse_args())

if args['action'] is None:
    print('--action is a mandatory argument. You cannot use this utility without --action argument')
    exit(1)

if args['action'] == 'list_hostedzones': # 'get_all_hosted_zones' action
    print(get_all_hosted_zones())

elif args['action'] == 'get_all_hosted_zones_count': # 'get_all_hosted_zones_count' action
    print(get_all_hosted_zones_count())

elif args['action'] == 'list_recordsets': # 'list_recordsets' action
    if args['hostedzone-id'] is None:
        print('--hostedzone-id is a mandatory argument for list_recordsets action')
        print('Example command for list_recordsets: --action list_recordsets --hostedzone-id HostedZoneID')
    else:
        list_resource_record_sets(args['hostedzone-id'], args['maxitems'])

elif args['action'] == 'create': # 'create' action
    if args['zone-name'] is None:
        print('--zone-name is a mandatory argument for create hosted zone action')
        print('Example command for create: --action create zone-name, comment, vpc-region, vpcid, private_zone=True|False')
    else:
        create_hosted_zone(args['--zone-name'], args['comment'], args['vpc-region'], args['vpcid'], args['private_zone'])

elif args['action'] == 'delete': # 'delete' action
    if args['hostedzone-id'] is None:
        print('--hostedzone-id is a mandatory argument for delete hosted zone action')
        print('Example command for delete: --action delete --hostedzone-id HostedZoneID')
    else:
        delete_hosted_zone(args['--hostedzone-id'])

