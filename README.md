## Overview
Do you need to deploy a canary test into your AWS account to be notified when certain IAM actions do not succeed? Are you concerned about sudden changes to IAM permission boundaries impacting your workloads? Do you need to detect IAM access misconfigurations not in your control such as overly restrictive AWS Organizations Service Control Policies (SCPs)?<br/>

This repository offers a simple Lambda function to routinely test IAM permissions using the IAM Policy Simulator API. The IAM Policy Simulator API performs a dry-run simulation by returning whether the requested actions would be allowed or denied without actually running any of the actions.<br/> 

The Lambda function demonstrates an examplatory implementation of an IAM canary test concept, where the check is for "Allow" effect. You can extend the code to implement a reverse canary test which fails when a permission is accidentally extended. In this case, the canary test routinely simulates particular IAM actions that should be denied.<br/> 

## Deployment
I deployed the Lambda function in my AWS test account using https://www.serverless.com/ and provided the serverless.yml for your reference. However, you can choose to deployed using any other preferred option such as AWS CodeDeploy or AWS CloudFormation. When using the serverless.yml file, update the principal source identifier and action list and also include your notification email address.<br/>

Alternatively, you can follow the link below to deploy the Lambda function as a .zip file archive.<br/>
Reference link: https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

## Environment
The Lambda function has no external dependencies other than Python 3.8. The Lambda requires access to action (iam:SimulatePrincipalPolicy) to run. The suggested timeout limit is 10 seconds. The function must be configured with two environment variable: (source_arn) and (action_names). The former is the Amazon Resource Name (ARN) of a user, group, or role whose policies you want to include in the test such as (arn:aws:iam::111111111111:role/MyAdminRole). The latter is a comma separated list of service identifiers and API operations to evaluate in the test such as (iam:CreateUser,iam:CreateAccessKey)   

## Testing
The core logic (other than the handler method) can be tested locally without the need for Lambda deployment. I provided two files (test.py and requirements.txt) to help you install and run the IAM canary check locally. You still need to have your AWS access credentials in .aws\credentials for the test script to work. Make sure to change the (source_arn) to your principal ARN designated for testing. 

## Cost
The total cost of the Lambda function is estimated to be less than $1 USD/month, when the Lambda and CloudWatch free usage tiers are not included. 

## Output
The Lambda function will throw an exception when the canary test fails. I suggest to consider triggering the Lambda function periodically, creating a CloudWatch alarm for the lambda function error metric, and configuring a notification email when the canary test fails. The serverless.yml file is provided to help you automatically configure these three steps with default values. When deploying using the serverless.yml file, you need to update the principal source identifier and action list and also include your notification email address.
