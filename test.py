import os
import handler

def test_iam_canary_check():
	print('### Test 1: handler.iam_canary_check...')
	os.environ['source_arn'] = 'arn:aws:iam::111111111111:role/Admin' # Change this to your principal arn
	os.environ['action_names'] = 'ec2:RunInstances'
	print(handler.iam_canary_check())
	os.environ['action_names'] = 'ec2:RunInstances,imagebuilder:CreateImagePipeline'
	print('### Test 2: iam_canary_check...')
	print(handler.iam_canary_check())
	print('### Test End!')

if __name__ == '__main__':
    test_iam_canary_check()