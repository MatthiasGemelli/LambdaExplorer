# LambdaExplorer
AWS Lambda Explorer  
by Matthias Gemelli, October 2017

# 0 - Context
While creating AWS Lambda functions for a custom Alexa skill and my 
[IntelliCam]<https://github.com/MatthiasGemelli/IntelliCam> 
I had to learn basic AWS interaction from within AWS Lambda.

# 1 - Platform Notes
The following AWS Lambda functions were written/tested with Python 2.7.
**Caution**
- Code does not contain any error handling (yet), e.g. for missing IAM permissions and the like.


# 2 - Setup & Test
- Simply log in to the AWS Console at https://console.aws.amazon.com/console/home
- Then create a new AWS Lambda function at https://console.aws.amazon.com/lambda/home
- "Create New Function", "Author from scratch", give it a name
- **Important: Give it an IAM role** with the necessary permissions (e.g. S3 Full Access, EC2 Full access...)
- Select Runtime: Python 2.7, enter the handler `lambda_function.lambda_handler`
- copy & paste the code below
- now Save and Test the new function
- Hopefully it shows "Execution result: succeeded(logs)" - now expand Details
- The Log output should now look like this:
```
START RequestId: 123123123-b68c-11e7-a47f-123123123 Version: $LATEST
XXX - Lambda Explorer - Inside Lambda Handler
XXX - Lambda Explorer - ENVIRONMENT start
XXX - ENVIRONMENT : LAMBDA_TASK_ROOT - /var/task
XXX - ENVIRONMENT : AWS_EXECUTION_ENV - AWS_Lambda_python2.7
XXX - ENVIRONMENT : LAMBDA_RUNTIME_DIR - /var/runtime
XXX - ENVIRONMENT : AWS_REGION - eu-west-1
XXX - ENVIRONMENT : AWS_LAMBDA_LOG_GROUP_NAME - /aws/lambda/gemelli_lambda_01
XXX - ENVIRONMENT : AWS_LAMBDA_LOG_STREAM_NAME - 2017/10/21/[$LATEST]38611069911549179d35a7ce6f8b3cbd
XXX - ENVIRONMENT : AWS_LAMBDA_FUNCTION_NAME - gemelli_lambda_01
XXX - ENVIRONMENT : AWS_LAMBDA_FUNCTION_MEMORY_SIZE - 128
XXX - ENVIRONMENT : AWS_LAMBDA_FUNCTION_VERSION - $LATEST
XXX - ENVIRONMENT : PATH - /usr/local/bin:/usr/bin/:/bin
XXX - ENVIRONMENT : LANG - en_US.UTF-8
XXX - ENVIRONMENT : PYTHONPATH - /var/runtime
XXX - ENVIRONMENT : TZ - :UTC
XXX - OS getuid   : 396
XXX - OS uname    : <built-in function uname>
XXX - OS curdir   : .
XXX - SYS platform: linux2
XXX - SYS version : 2.7.12 (default, Sep  1 2016, 22:14:00) 
[GCC 4.8.3 20140911 (Red Hat 4.8.3-9)]
XXX - SYS vers inf: sys.version_info(major=2, minor=7, micro=12, releaselevel='final', serial=0)
XXX - Lambda Explorer - ENVIRONMENT end
XXX - Lambda Explorer - Done for now.
END RequestId: 123123123-b68c-11e7-a47f-123123123
REPORT RequestId: 123123123-b68c-11e7-a47f-123123123	Duration: 0.91 ms	Billed Duration: 100 ms 	Memory Size: 128 MB	Max Memory Used: 25 MB	
```
#3 - Troubleshooting
The Log output is typically very explicit and identifies the lines with the offending code. 
I had to increase the timeout from 3 secs to 3 minutes, as some Boto interactions were exceeding the timeout limit.

#4 - AWS Lambda Explorer Code (Python 2.7)
```
# AWS Lambda Lambada - Matthias Gemelli - rev02 (from Blueprint Pyton27-S3)
from __future__ import print_function
print('XXX - Lambda Explorer Starting Up...')
import json
import urllib
import boto3
import os
import sys



def mylambda_ec2(event):   #get my EC2 instances - exceeds 3 sec timeout!!
    #http://boto3.readthedocs.io/en/latest/guide/migrationec2.html
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

            #instance.stop()
    return 'XXX - Lambda Explorer - AWS EC2 done'

def mylambda_environment():   #get AWS Environment Variables
    print ('XXX - Lambda Explorer - ENVIRONMENT start')
    # http://docs.aws.amazon.com/lambda/latest/dg/current-supported-versions.html
    reserved = ['LAMBDA_TASK_ROOT','AWS_EXECUTION_ENV','LAMBDA_RUNTIME_DIR',
        'AWS_REGION','AWS_LAMBDA_LOG_GROUP_NAME','AWS_LAMBDA_LOG_STREAM_NAME',
        'AWS_LAMBDA_FUNCTION_NAME','AWS_LAMBDA_FUNCTION_MEMORY_SIZE',
        'AWS_LAMBDA_FUNCTION_VERSION','PATH','LANG','PYTHONPATH','TZ']
    for env in reserved:
        print('XXX - ENVIRONMENT : ' + env + ' - ' + os.environ[env])
    print    ('XXX - OS getuid   : ' + str(os.getuid()))
    print    ('XXX - OS uname    : ' + str(os.uname))
    print    ('XXX - OS curdir   : ' + str(os.path.curdir))
    print    ('XXX - SYS platform: ' + str(sys.platform))
    print    ('XXX - SYS version : ' + str(sys.version))
    print    ('XXX - SYS vers inf: ' + str(sys.version_info))
    return 'XXX - Lambda Explorer - ENVIRONMENT end'

def mylambda_modules():       # get LAmbda Python Modules
    # inspired by https://gist.github.com/gene1wood/4a052f39490fae00e0c3
    print    ('XXX - Lambda Explorer - MODULES start')
    for module in sys.builtin_module_names:
        print ('XXX - Python Module: ' + str(module) )
    return 'XXX - Lambda Explorer - MODULES end'

def mylambda_services():     # get AWS Lambda services info
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

def mylambda_s3(event):        #get AWS S3 details - e.g. from S3 trigger
    print ('XXX - Lambda Explorer - S3 start')
    s3_bucket   = event['Records'][0]['s3']['bucket']['name']
    s3_key      = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    print    ('XXX - S3 bucket: ' + s3_bucket)
    print    ('XXX - S3 key   : ' + s3_key)
    return 'XXX - Lambda Explorer - S3 end'

# My Event Parser - adjust to your needs, e.g. S3 vs. EC2 provides different info
def mylambda_event_parser(event):
    print ('XXX - Lambda Explorer - Event Parser Start ')
    event_source= event['Records'][0]['eventSource']
    event_name  = event['Records'][0]['eventName']
    event_time  = event['Records'][0]['eventTime']
    event_srcip = event['Records'][0]['requestParameters']['sourceIPAddress'] 
    event_regio = event['Records'][0]['awsRegion']
    event_user  = event['Records'][0]['userIdentity']
    s3_bucket   = event['Records'][0]['s3']['bucket']['name']
    s3_key      = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    print("XXX Lambda Event Info  : \n" + str(event))
    print("XXX Lambda Event Source: ", event_source)
    print("XXX Lambda Event Name  : ", event_name)
    print("XXX Lambda Event Time  : ", event_time)
    print("XXX Lambda Event Src IP: ", event_srcip)
    print("XXX Lambda Event Region: ", event_regio)
    print("XXX Lambda Event User  : ", event_user)
    print("XXX Lambda S3 bucket   : ", s3_bucket)
    print("XXX Lambda S3 key      : ", s3_key)
    print ('XXX - Lambda Explorer - Event Parser Start ')
    return 'XXX - Lambda Explorer - Event Parser End '

def lambda_handler(event, context):
    print ("XXX - Lambda Explorer - Inside Lambda Handler")
    #comment/uncomment the following lines to retrieve different info
    
    #print (mylambda_event_parser(event))  # parse the event data, e.g. S3 bucket/key
    #print (mylambda_services())           # list AWS services and regions
    #print (mylambda_environment())        # retrieve some ENVIRONMENT info
    #print (mylambda_modules())            #retrieve list of Python Modules
    #print (mylambda_s3(event))            #get AWS S3 details - requires permissions!!
    print (mylambda_ec2(event))           #get AWS EC2 details - requires permissions!!
    #print (mylambda_ec2instance('i-05d13b99db20b8ab4', 'sa-east-1'))
 
    print ("XXX - Lambda Explorer - Done for now.")
```