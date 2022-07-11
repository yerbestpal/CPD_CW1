import boto3
import os
import time

# Iterates through the files in the given local path using a for loop. Each file in that directory is uploaded to the given S3 Bucket with a break of 30
def upload_files(path):
	session = boto3.Session()
	s3 = session.resource('s3')
	bucket = s3.Bucket('bucket-s2030507')
	for subdir, files in os.walk(path):
		for file in files:
			full_path = os.path.join(subdir, file)
			with open(full_path, 'rb') as data:
				bucket.put_object(Key=full_path[len(path) + 1 :], Body=data)
				time.sleep(30)

# Calls function to upload files to S3 Bucket
upload_files('images')