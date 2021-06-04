import os
import json
import boto3

# lambda handler for canary test of allowed and denied principles actions 
def check_principals_actions(event, context): 
    return read_and_simulate_principals_actions()

# read effects, principles, and actions to check IAM entity permissions
def read_and_simulate_principals_actions():
    input_json = os.environ.get("principals_actions_json")
    dictionary = json.loads(input_json)
    
    allowed_pairs = dict()
    denied_pairs = dict()

    if "allowed_pairs" in dictionary:
        allowed_pairs = dictionary["allowed_pairs"]

    if "denied_pairs" in dictionary:
        denied_pairs = dictionary["denied_pairs"]    

    for key in allowed_pairs:
        simulate_principal_actions(key, allowed_pairs[key], True)

    for key in denied_pairs:
        simulate_principal_actions(key, denied_pairs[key], False)

    return "Completed test of " + str(len(allowed_pairs)) + " allowed pairs and " + str(len(denied_pairs)) + " denied pairs"     
    
# check if one principal is allowed (effect_allow = true) or denied (effect_allow = false) on all actions
def simulate_principal_actions(principal_arn, action_names, effect_allow):
    client = boto3.client("iam")
    result = client.simulate_principal_policy(PolicySourceArn=principal_arn, ActionNames=tuple(action_names.split(",")))

    input_string = "effect_allow=" + str(effect_allow) + ", principal_arn=" + principal_arn + ", action_names=" + action_names

    for decision in (result["EvaluationResults"]):
        if effect_allow and "Deny" in decision["EvalDecision"]:
            raise Exception("Failed allow test: " + input_string)
        elif not effect_allow and decision["EvalDecision"] == "allowed":
            raise Exception("Failed deny test: " + input_string)
        
    return "Completed test: " + input_string