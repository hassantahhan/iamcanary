## Overview
Do you need to deploy a canary into your AWS account to test when certain IAM actions succeed? Are you concerned about sudden changes to permission boundaries impacting your workloads? Do you need a tool to help you discover concerning misconfigurations such as changes to AWS Organizations Service Control Policies (SCPs) not in your control?<br/>

The Lambda function tool tests IAM policies using the IAM policy simulator API, which performs a dry-run and does not simulate running the selected actions and only returns whether the requested action would be allowed or denied.<br/> 

The Lambda function demonstrates a concept which can be implemented in reverse to test when a permission is accidentally extended. In this case, the canary routinely attempts particular API actions that should be denied.<br/> 

## Deployment
I deployed the Lambda function in my AWS test account using https://www.serverless.com/ and provided the serverless.yml for your reference. However, you can choose to deployed using any other preferred option such as AWS CodeDeploy or AWS CloudFormation. When using the serverless.yml file, update the principal source arn and action list and also include your notification email address.<br/>

Alternatively, you can follow the link below to deploy the Lambda function as a .zip file archive.<br/>
Reference link: https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

## Environment
The Lambda function has no external dependencies other than Python 3.8. The Lambda requires access to action (iam:SimulatePrincipalPolicy) to run. The suggested timeout limit is 10 seconds. The function must be configured with two environment variable: (source_arn) and (action_names). The former is the Amazon Resource Name (ARN) of a user, group, or role whose policies you want to include in the test such as (arn:aws:iam::111111111111:role/Admin). The latter is a comma separated list of service identifiers and API operations to evaluate in the test such as (iam:CreateUser,iam:CreateAccessKey)   

## Testing
The core logic (other than the handler method) can be tested locally without the need for Lambda deployment. I provided two files (test.py and requirements.txt) to help you install and run the IAM canary check locally. You still need to have your AWS access credentials in .aws\credentials for the test script to work. Make sure to change the (source_arn) to your principal arn designated for testing. 

## Cost
The total cost of the Lambda function is estimated to be less than $1 USD/month, when the Lambda and CloudWatch free usage tiers are not included. 

## Output
The Lambda function will throw an exception when the canary test fails. I suggest to consider triggering the Lambda function periodically, creating a CloudWatch alarm for the lambda function error metric, and configuring a notification email when the canary fails. The serverless.yml file is provided to help you automatically configure these three steps. When deploying using the serverless.yml file, you need to update the principal source arn and action list and also include your notification email address.
