import os
import boto3

# check if principal is allowed on all actions
def check_all_allowed():
	source_arn = os.environ.get('source_arn')
	action_names = os.environ.get('action_names')

	client = boto3.client('iam')
	result = client.simulate_principal_policy(PolicySourceArn=source_arn, ActionNames=tuple(action_names.split(',')))

	all_allowed = None

	for decision in (result['EvaluationResults']):
		if all_allowed == None:
			all_allowed = decision['EvalDecision'] == 'allowed'
		elif 'Deny' in decision['EvalDecision']:
			all_allowed = False

	value_string = 'all_allowed=' + str(all_allowed) + ', source_arn=' + source_arn + ', action_names=' + action_names

	if not all_allowed:
		raise Exception('Failed IAM Canary Test: ' + value_string)
	return 'Completed IAM Canary Test: ' + value_string

# check if principal is denied on all actions
def check_all_denied():
	source_arn = os.environ.get('source_arn')
	action_names = os.environ.get('action_names')

	client = boto3.client('iam')
	result = client.simulate_principal_policy(PolicySourceArn=source_arn, ActionNames=tuple(action_names.split(',')))

	all_denied = None
	
	for decision in (result['EvaluationResults']):
		if all_denied == None:
			all_denied = 'Deny' in decision['EvalDecision']
		elif decision['EvalDecision'] == 'allowed':
			all_denied = False

	value_string = 'all_denied=' + str(all_denied) + ', source_arn=' + source_arn + ', action_names=' + action_names

	if not all_denied:
		raise Exception('Failed IAM Canary Test: ' + value_string)
	return 'Completed IAM Canary Test: ' + value_string

# lambda handler for action allowed canary test 
def canary_test_allowed(event, context): 
    return check_all_allowed()

# lambda handler for action denied canary test 
def canary_test_denied(event, context): 
    return check_all_denied()