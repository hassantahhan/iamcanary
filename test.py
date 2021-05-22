import os
import handler

# Change test_principal, test_actions, and test_full_json to match your environment
test_principal = "arn:aws:iam::111111111111:role/Admin"
test_1_actions = "ec2:RunInstances"
test_2_actions = "ec2:RunInstances,imagebuilder:CreateImagePipeline"
test_3_actions = "imagebuilder:CreateImagePipeline"
test_4_actions = "imagebuilder:CreateImagePipeline,ec2:RunInstances"
test_full_json = '{"arn:aws:iam::111111111111:role/Admin":"imagebuilder:CreateImagePipeline",' \
                 '"arn:aws:iam::111111111111:role/Read":"imagebuilder:CreateImagePipeline"}'

def test_check_one_principal_actions():
    print("### test_check_one_principal_actions() started")
        
    print("? Test 1: check_one_principal_actions(allowed)...")
    try:
        print(handler.check_one_principal_actions(test_principal, test_1_actions, True))
    except Exception as e:
        print(e)

    print("? Test 2: check_one_principal_actions(allowed)...")
    try:
        print(handler.check_one_principal_actions(test_principal, test_2_actions, True))
    except Exception as e:
        print(e)
    
    print("? Test 3: check_one_principal_actions(denied)...")
    try:
        print(handler.check_one_principal_actions(test_principal, test_3_actions, False))
    except Exception as e:
        print(e)
        
    print("? Test 4: check_one_principal_actions(denied)...")
    try:
        print(handler.check_one_principal_actions(test_principal, test_4_actions, False))
    except Exception as e:
        print(e)

    print("### test_check_one_principal_actions() ended!")

def test_check_all_principals_actions():
    print("### test_check_all_principals_actions() started")
    os.environ['principals_actions_json'] = test_full_json
        
    print("? Test 1: check_all_principals_actions(allowed)...")
    try:
        print(handler.check_all_principals_actions(True))
    except Exception as e:
        print(e)

    print("? Test 2: check_all_principals_actions(denied)...")
    try:
        print(handler.check_all_principals_actions(False))
    except Exception as e:
        print(e)
        
    print("### test_check_all_principals_actions() ended!")

if __name__ == "__main__":
    test_check_one_principal_actions()
    test_check_all_principals_actions()