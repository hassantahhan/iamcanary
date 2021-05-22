import os
import json
import boto3

# lambda handler for canary test of allowed actions 
def canary_test_allowed(event, context): 
    return check_all_principals_actions(True)

# lambda handler for canary test of denied actions
def canary_test_denied(event, context): 
    return check_all_principals_actions(False)

# check by order if all principals have the allowed or denied effect on all actions
def check_all_principals_actions(effect_allow):
    input_json = os.environ.get("principals_actions_json")
    dictionary = json.loads(input_json)

    for key in dictionary:
        check_one_principal_actions(key, dictionary[key], effect_allow)
 
    if effect_allow:
        return "Completed IAM Canary Test of Allowed Actions: " + input_json   
    else:
        return "Completed IAM Canary Test of Denied Actions: " + input_json

# check if one principal is allowed (effect_allow = true) or denied (effect_allow = false) on all actions
def check_one_principal_actions(principal_arn, action_names, effect_allow):
    client = boto3.client("iam")
    result = client.simulate_principal_policy(PolicySourceArn=principal_arn, ActionNames=tuple(action_names.split(",")))

    input_string = "principal_arn=" + principal_arn + ", action_names=" + action_names

    for decision in (result["EvaluationResults"]):
        if effect_allow and "Deny" in decision["EvalDecision"]:
            raise Exception("Failed IAM Canary Test of Allowed Actions: " + input_string)
        elif not effect_allow and decision["EvalDecision"] == "allowed":
            raise Exception("Failed IAM Canary Test of Denied Actions: " + input_string)
        
    if effect_allow:
        return "Completed IAM Canary Test of Allowed Actions: " + input_string   
    else:
        return "Completed IAM Canary Test of Denied Actions: " + input_string