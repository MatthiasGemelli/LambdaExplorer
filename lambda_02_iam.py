# AWS Lambda Lambada - Matthias Gemelli - rev02 (from Blueprint Pyton27-S3)
from __future__ import print_function
print('XXX - Loading Lambda Explorer')
import json
import urllib
import boto3


def mylambda_userdetails(user_list):
    iam      = boto3.client('iam')      
    for user in user_list:
        iam_usr  = iam.get_user(UserName=user)['User']
        print ('XXX - User Details for : ' + str(user))
        for param in ['UserName', 'UserId','CreateDate','Arn']:   #interesting user info
                    print ('    -> ' + param + ' : ' + str(iam_usr[param]))
    return 'XXX - Lambda Explorer - IAM User Details Done'

def mylambda_roledetails(role_list):
    iam      = boto3.client('iam')      
    for role in role_list:
        iam_role      = iam.get_role(RoleName=role)['Role']
        print ('XXX - Role Details for : ' + str(role))
        for param in ['RoleName', 'RoleId', 'CreateDate', 'Arn']:   #interesting user info
                    print ('    -> ' + param + ' : ' + str(iam_role[param]))

        #second get Role IAM Policies
        iam_role_pols = iam.list_attached_role_policies(RoleName=role)
        for policy in iam_role_pols['AttachedPolicies']:
            print ('    -> attached policy: ' +  str(policy['PolicyName']))  # 'PolicyArn'
        
    return 'XXX - Lambda Explorer - IAM Role Details Done'


def mylambda_iam_list_users():    
    print ('XXX - IAM List Users')
    #http://boto3.readthedocs.io/en/latest/guide/iam-example-managing-users.html

    userlist  = []
    iam = boto3.client('iam')       #no AWS defined IAM read access policy?
    paginator = iam.get_paginator('list_users')  # list users with pagination interface
    for response in paginator.paginate():
        for user in response['Users']:
            #print (str(user))
            userlist.append(str(user['UserName']))
            print ('XXX - User Details: ' + str(user['UserName']))
            for param in ['UserId', 'CreateDate','Arn']:   #interesting user info
                print ('    -> ' + param + ' : ' + str(user[param]))
    return userlist

def mylambda_iam_list_roles():    
    print ('XXX - IAM List Roles')
    rolelist = []
    iam      = boto3.client('iam')      
    paginator = iam.get_paginator('list_roles')  # list users with pagination interface
    for response in paginator.paginate():
        for role in response['Roles']: 
            #print (str(role))
            rolelist.append(str(role['RoleName']))
            print ('XXX - Role Details: ' + str(role['RoleName']))
            for param in ['RoleId', 'CreateDate','Arn']:   #interesting role info
                print ('    -> ' + param + ' : ' + str(role[param]))
    return rolelist  #little array/list
    
def mylambda_iam_CredentialReport():   
    print ('XXX - IAM Credential Report')
    iam      = boto3.client('iam')      
    iam_cred_report = iam.get_credential_report()  # new one every 4 hrs
    #print (iam_cred_report)    #check the raw format first...
    print ('XXX - IAM Credential Report Format : ' + str(iam_cred_report['ReportFormat']))
    print ('XXX - IAM Credential Report Time   : ' + str(iam_cred_report['GeneratedTime']))
    #print ('XXX - IAM Credential Report Content: \n ' + str(iam_cred_report['Content']))
    #probably better to save directly into a CSV file on S3...

    for line in iam_cred_report['Content'].splitlines():
        #print('    -> ' + line)  # CSV line
        iam_usr    = str(line.split(',')[0])   #username
        iam_arn    = str(line.split(',')[1])   # ARN
        iam_create = str(line.split(',')[2])   # user created
        iam_pwuse  = str(line.split(',')[4])   #PW last used
        iam_pwchg  = str(line.split(',')[5])   #PW last changed
        print ('    - ' + iam_usr + ' ' + iam_create + ' ' + iam_pwuse)
    return 'XXX - IAM Credential Report done'
    


def lambda_handler(event, context):
    print (mylambda_iam_CredentialReport()) 
    users = mylambda_iam_list_users()
    roles = mylambda_iam_list_roles()
    
    print (mylambda_userdetails(users))
    print (mylambda_roledetails(roles))
    
    
    #the end - nothing further below here
    
