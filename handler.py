import os
import boto3

def iam_canary_check():
	source_arn = os.environ.get('source_arn')
	action_names = os.environ.get('action_names')

	client = boto3.client('iam')
	result = client.simulate_principal_policy(PolicySourceArn=source_arn, ActionNames=tuple(action_names.split(',')))

	allowed = None
	for decision in (result['EvaluationResults']):
		if decision['EvalDecision'] == 'allowed' and allowed == None:
			allowed = True
		elif 'Deny' in decision['EvalDecision']:
			allowed = False

	value_string = '[allowed=' + str(allowed) + ', source_arn=' + source_arn + ', action_names=' + action_names +']'	

	if not allowed:
		raise Exception('Failed iam_canary_check ' + value_string)
	return 'Successfully completed iam_canary_check ' + value_string

def handler(event, context): 
    return iam_canary_check()