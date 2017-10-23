# Matthias Gemelli, Oct 2017
# inspired by http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/LogEC2InstanceState.html
# and my previous Lambda experiments at https://github.com/MatthiasGemelli/LambdaExplorer
# Setup: create this LAMBDA first, then Clooudwatch Event on EC2 state change. 
# Caution: EC2, Cloudwatch event and Lambda need to be in the same region!
# check your Cloudwatch logs for output of the Lambda function...

from __future__ import print_function
print('XXX - LAMBDA EC2 Recovery - triggered by Cloudwatch Event')

#import json
#import urllib
import boto3

def mylambda_ec2_start(instance_id, region):
    print ('XXX - EC2 Recovery: Restart of ' + instance_id + ' in region: ' + region)
    #HAHA!! you can stop my EC2 instance as often as you want!
    ec2 = boto3.resource('ec2', region_name=region)
    instance = ec2.Instance(instance_id)
    instance.start()
    print ('XXX - XXX INSTANCE SHOULD BE STARTING NOW!!   XXX')
    return None

def mylambda_event_parser(event):
    #print ('XXX - Lambda Event Info  :\n' + str(event))
    event_region = 'no region'
    event_detail = {}
    event_dtl_tp = 'no detail type'
    event_source = 'no source'
    event_resour = 'no resources'
    
    #have to check if keys exist before reading them...different event syntax
    #print ('XXX - Lambda Event Keys  : '  + str(event.keys()))
    if 'region'      in event.keys(): event_region = event['region']
    if 'detail'      in event.keys(): event_detail = event['detail']
    if 'detail-type' in event.keys(): event_dtl_tp = event['detail-type']
    if 'source'      in event.keys(): event_source = event['source']
    if 'resources'   in event.keys(): event_resour = event['resources']
    #print ('XXX - EC2 Recovery - Region       : ' + str(event_region))
    #print ('XXX - EC2 Recovery - Detail Type  : ' + str(event_dtl_tp))
    #print ('XXX - EC2 Recovery - Source       : ' + str(event_source))
    
    if event_source == 'aws.ec2':
        if ('state' in event_detail.keys()) and ('instance-id' in event_detail.keys()):
                #print ('XXX - EC2 Recovery ---> State     : ' + event_detail['state'])
                #print ('XXX - EC2 Recovery ---> Instance  : ' + event_detail['instance-id'])
                if (event_detail['state']) == 'stopping': print ('XXX - EC2 Recovery: stopping --> do nothing')
                if (event_detail['state']) == 'pending' : print ('XXX - EC2 Recovery: pending  --> do nothing')
                if (event_detail['state']) == 'running' : print ('XXX - EC2 Recovery: running  --> do nothing')
                if (event_detail['state']) == 'stopped' :   #Haha! Gotcha! 
                    mylambda_ec2_start(event_detail['instance-id'], event_region)
                
    return 'event parser done'

def lambda_handler(event, context):
    text = mylambda_event_parser(event)
    print('XXX - LAMBDA EC2 Recovery DONE')
    #nothing to see here...
