# LambdaExplorer
a collection of AWS blueprints running on Python 2.7 for usage within AWS Lambda.   
by Matthias Gemelli, October 2017

# 0 - Context
While creating AWS Lambda functions for a custom Alexa skill and my 
[IntelliCam]<https://github.com/MatthiasGemelli/IntelliCam> 
I had to learn basic AWS interaction from within AWS Lambda.

# 1 - Platform Notes
The following AWS Lambda functions were written/tested with Python 2.7.  

**Caution:** Code does not contain any error handling (yet), e.g. for missing IAM permissions and the like.


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
# 3 - Troubleshooting
- Log output is typically very explicit and identifies the lines with the offending code. 
- had to increase the timeout from 3 secs to 3 minutes, as some Boto interactions were exceeding the default of 3 seconds
- the IAM role associated with Lambda requires necessary permissions - for testing I gave it more than required   
(e.g. AmazonEC2FullAccess, AmazonS3FullAccess, AWSLambdaExecute...)

# 4 - AWS Lambda Explorer Code (Python 2.7)
## 4.1 Lambda 01 - Event Parser & Environment 
Parses event information (e.g. the S3 bucket/key that triggered the Lambda).  
**Caution** Event structure differs between triggers (e.g. had to completely re-do for a Cloudwatch trigger. see below)  

Code at https://github.com/MatthiasGemelli/LambdaExplorer/blob/master/lambda_01_env.py

## 4.2 Lambda 02 - EC2 Scanner
Scans all regions for EC2 instances and displays information about each instance.  
Code contains no error handling or pagination (e.g. adjust if you handlde large number of EC2 instances)  

Code at https://github.com/MatthiasGemelli/LambdaExplorer/blob/master/lambda_02_ec2.py

## 4.3 Lambda 03 - IAM Scanner
Iterate through users and roles and displays their details.  

Code at https://github.com/MatthiasGemelli/LambdaExplorer/blob/master/lambda_03_iam.py

## 4.4 Lambda 04 - EC2 Shutdown Recovery
Inspired by someone else's nightly EC2 shutdown, I created this EC2 recovery Lambda.  
Using a Cloudwatch rule as trigger as per  http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/LogEC2InstanceState.html


Code at https://github.com/MatthiasGemelli/LambdaExplorer/blob/master/lambda_04_ec2_recov.py


## 4.5 Lambda 05 - RDS, S3, Lightsail Scanner
Coming soon...

