# aws-utility-tool

This is a docker cli tool used to perform admin level operations using the [AWS SDK](https://aws.amazon.com/sdk-for-python/) for service such as 
route53, s3 

<!-- TOC -->

- [Usage](#usage)
- [Examples](#examples)
    - [Determine who you are when connecting to AWS](#determine-who-you-are-when-connecting-to-aws)
    - [Run cli commands to use s3 service](#run-s3-script-with )
    - [Run cli commands to use route53 service](#run-route53-script-with )

<!-- /TOC -->

## Usage

Begin by running 
*   `./build.sh ACCESS_KEY_ID=<AWS User Key> SECRET_ACCESS_KEY=<AWS User Secret>`
*   `./run_s3.sh` aws cli commands for S3 service 
    * It contains:
        * `list` list all s3 buckets
        * `create_bucket` create a S3 bucket
        * `upload_file` upload a file with file_path to a S3 bucket
*   `./run_route53.sh` aws cli commands for route53 service 
    * It contains:
        * `list_hostedzones` list all hosted zones
        * `list_recordsets` list all record sets for a given hosted zone Id
        * `create` create a hosted zone
        * `delete` delete a hosted zone of a give hosted zone Id
        
## Examples

#### Determine who you are when connecting to AWS

* You will a user with programmatic access that enables you to have access key ID and secret access key
* You must have permissions to with right policies to access following services to perform list, create and delete actions
    * s3
    * route53
* You will use the access key ID and secret to build docker image 
```bash
$ ./build.sh ACCESS_KEY_ID=XXXXXXXXXXX SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXX
```

#### Run S3 script with 
`$ ./run_s3.sh`

help: 
`$ ./run_s3.sh -h`

##### Examples 
list all s3 buckets:
`$ ./run_s3.sh --action list`

create s3 bucket:
`$ ./run_s3.sh --action create_bucket --acl ACL --bucket BUCKET_NAME --region REGION`

upload file: 
`$ ./run_s3.sh --action upload_file --filpath FILEPATH --bucket BUCKET_NAME --region REGION --acl ACL`


#### Run route53 script with 
`$ ./run_route53.sh`

help: 
`$ ./run_route53.sh -h`

##### Examples 

list all hosted zone: 
`./run_route53.sh --action list_hostedzones`

delete a hosted zone:
`./run_route53.sh --action delete --hostedzoneid HOSTEDZONEID`

create a new hosted zone:
`./run_route53.sh --action create --name HOSTEDZONE-NAME.com --comment COMMENT --vpc_region REGION --vpcid REGIONID --private_zone TRUE|FALSE`