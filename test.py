import os
import handler

def test_iam_canary_check():
	print('### Test Start!')

	# Change source_arn to your principal arn
	os.environ['source_arn'] = 'arn:aws:iam::111111111111:role/Admin' 
		
	print('### Test 1: check_all_allowed...')
	try:
		os.environ['action_names'] = 'ec2:RunInstances'
		print(handler.check_all_allowed())
	except Exception as e:
		print(e)

	print('### Test 2: check_all_allowed...')
	try:
		os.environ['action_names'] = 'ec2:RunInstances,imagebuilder:CreateImagePipeline'
		print(handler.check_all_allowed())
	except Exception as e:
		print(e)
	
	print('### Test 3: check_all_denied...')
	try:
		os.environ['action_names'] = 'imagebuilder:CreateImagePipeline'
		print(handler.check_all_denied())
	except Exception as e:
		print(e)
		
	print('### Test 4: check_all_denied...')
	try:
		os.environ['action_names'] = 'ec2:RunInstances,imagebuilder:CreateImagePipeline'
		print(handler.check_all_denied())
	except Exception as e:
		print(e)

	print('### Test End!')

if __name__ == '__main__':
    test_iam_canary_check()