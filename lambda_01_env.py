# AWS Lambda Lambada - Matthias Gemelli - rev03 (from Blueprint Pyton27-S3)
# with Event Parser, Lambda  Environment, AWS Service & Regions,
# EC2 scanner
# coming soon: S3 scanner, RDS scan, SG/VPC scan, Lightsail

from __future__ import print_function
print('XXX - Lambda Explorer Starting Up...')
import json
import urllib
import boto3
import os
import sys

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
    s3_bucket   = event['Records'][0]['s3']['bucket']['name']
    s3_key      = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    print    ('XXX Lambda Event - S3 bucket: ' + s3_bucket)
    print    ('XXX Lambda Event - S3 key   : ' + s3_key)

    print ('XXX - Lambda Explorer - Event Parser Start ')
    return 'XXX - Lambda Explorer - Event Parser End '

def lambda_handler(event, context):
    print ("XXX - Lambda Explorer - Inside Lambda Handler")
    #comment/uncomment the following lines to retrieve different info
    
    print (mylambda_event_parser(event))  # parse the event data, e.g. S3 bucket/key
    print (mylambda_environment())        # retrieve some ENVIRONMENT info
    print (mylambda_modules())            #retrieve list of Python Modules

    print ("XXX - Lambda Explorer - Done for now.")
