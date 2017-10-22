# AWS Lambda Lambada - Matthias Gemelli - rev02 (from Blueprint Pyton27-S3)
from __future__ import print_function
print('XXX - Loading Lambda Explorer')
import json
import urllib
import boto3

def mylambda_services():
    # http://boto3.readthedocs.io/en/latest/reference/core/session.html
    print ('XXX - Lambda Explorer - AWS Services Start')
    session    = boto3.session.Session()
    partitions = session.get_available_partitions()  # 'aws','aws-cn', aws-us-gov'
    services   = session.get_available_services()    #s3, ec2, ... load with boto.client('s3')
    resources  = session.get_available_resources()   # ...load with boto.resource()
    print ('XXX - Lambda Services: ' + str(services))      #print out all services...long list
    for service in ['s3','ec2']:                     #only 1..2, otherwise exceeds Lambda timeout
        regions = session.get_available_regions(service, partition_name='aws')
        print ('XXX - AWS Service ' + service + ' available in ' + str(regions))
    return 'XXX - Lambda Explorer - AWS Services End'

def mylambda_ec2(event):   #get my EC2 instances - exceeds 3 sec timeout!!
    #http://boto3.readthedocs.io/en/latest/guide/migrationec2.html
    #http://boto3.readthedocs.io/en/latest/reference/services/ec2.html#instance
    print ('XXX - Lambda Explorer - AWS EC2 starting')
    client = boto3.client('ec2')
    region_iterator = client.describe_regions()['Regions']
    for region in region_iterator:
        #print ('Looking for EC2 instances in: ' + str(region['RegionName']))
        ec2 = boto3.resource('ec2', region_name=region['RegionName']) 
        instance_iterator = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        for instance in instance_iterator:
            print ('XXX - Found EC2 : ' + str(instance.id)    + ' Type: ' + str(instance.instance_type) + ' in region: ' + str(region['RegionName']))
            print ('    -  in State : ' + str(instance.state) + ' Reason: ' + str(instance.state_reason))
            print ('    -  Launched : ' + str(instance.launch_time) + ' architecture: ' + str(instance.architecture))
            print ('    -  with  IP : ' + str(instance.private_ip_address) + ' and public IP: ' +str(instance.public_ip_address)) 
            print ('    -  Sec Grps : ' + str(instance.security_groups))
            print ('    -       VPC : ' + str(instance.vpc_id))
            #http://boto3.readthedocs.io/en/latest/reference/services/ec2.html#EC2.Instance.console_output
            #print ('    -  Console  :\n' + str(instance.console_output(DryRun=False)))

            #instance.stop()  #or .start() .terminate()
    return 'XXX - Lambda Explorer - AWS EC2 done'


def lambda_handler(event, context):
    # ----------PARSE EVENT data, context contains no useful data
    print ("XXX - Lambda Explorer - Inside Lambda Handler")
    print (mylambda_ec2(event))         # scans all regions for EC2 instances 
    print (mylambda_services())           # list AWS services and regions
    print ("XXX - Lambda Explorer - Finishing the Lambda Handler")
