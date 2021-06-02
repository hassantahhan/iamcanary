import os
import json
import handler

# Change test_principal, test_actions, and test_full_json to match your environment
def test_simulate_principal_actions():
    print("\n### test_simulate_principal_actions() started")
        
    print("\nTest 1: simulate_principal_actions(allowed)...")
    try:
        test_principal = "arn:aws:iam::111111111111:role/EC2Admin"
        test_actions = "ec2:RunInstances"
        print(handler.simulate_principal_actions(test_principal, test_actions, True))
    except Exception as e:
        print(e)

    print("\nTest 2: simulate_principal_actions(allowed)...")
    try:
        test_principal = "arn:aws:iam::111111111111:role/EC2Admin"
        test_actions = "imagebuilder:CreateImagePipeline"
        print(handler.simulate_principal_actions(test_principal, test_actions, True))
    except Exception as e:
        print(e)
    
    print("\nTest 3: simulate_principal_actions(allowed)...")
    try:
        test_principal = "arn:aws:iam::111111111111:role/EC2Admin"
        test_actions = "ec2:RunInstances,imagebuilder:CreateImagePipeline"
        print(handler.simulate_principal_actions(test_principal, test_actions, True))
    except Exception as e:
        print(e)
        
    print("\nTest 4: simulate_principal_actions(denied)...")
    try:
        test_principal = "arn:aws:iam::111111111111:role/EC2Admin"
        test_actions = "imagebuilder:CreateImagePipeline,ec2:RunInstances"
        print(handler.simulate_principal_actions(test_principal, test_actions, False))
    except Exception as e:
        print(e)

    print("\nTest 5: simulate_principal_actions(denied)...")
    try:
        test_principal = "arn:aws:iam::111111111111:role/EC2Admin"
        test_actions = "ec2:RunInstances,imagebuilder:CreateImagePipeline"
        print(handler.simulate_principal_actions(test_principal, test_actions, False))
    except Exception as e:
        print(e)

    print("\nTest 6: simulate_principal_actions(denied)...")
    try:
        test_principal = "arn:aws:iam::111111111111:role/EC2Run"
        test_actions = "imagebuilder:CreateImagePipeline"
        print(handler.simulate_principal_actions(test_principal, test_actions, False))
    except Exception as e:
        print(e)
    print("\n### test_simulate_principal_actions() ended!")

def test_read_and_simulate_principals_actions():
    print("\n### test_read_and_simulate_principals_actions() started")
    test_json = {
                    "allowed_pairs": {
                        "arn:aws:iam::111111111111:role/EC2Admin": "ec2:RunInstances,imagebuilder:CreateImagePipeline",
                        "arn:aws:iam::111111111111:role/EC2Run": "ec2:RunInstances"
                    },
                    "denied_pairs": {
                        "arn:aws:iam::111111111111:role/EC2Run": "imagebuilder:CreateImagePipeline"
                    }
                }
    os.environ['principals_actions_json'] = json.dumps(test_json)
    
    print("\nTest 1: read_and_simulate_principals_actions()...")
    try:
        print(handler.read_and_simulate_principals_actions())
    except Exception as e:
        print(e)
        
    print("\n### test_read_and_simulate_principals_actions() ended!")

if __name__ == "__main__":
    test_simulate_principal_actions()
    test_read_and_simulate_principals_actions()