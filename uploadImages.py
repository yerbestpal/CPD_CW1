import os
import time
import boto3
import logging
from botocore.exceptions import ClientError

# logger config.
logger = logging.getLogger()
logging.basicConfig(
  level=logging.INFO,
  format='%(asctime)s: %(levelname)s: %(message)s'
)

# Loop through images and upload to S3 bucket with a 30 second delay between uploads.
def upload_images(dir):
  session = boto3.Session()
  s3 = session.resource('s3')
  bucket = s3.Bucket('bucket-s2030507')
  for subdir, dirs, files in os.walk(dir):
    for file in files:
      dir_path = os.path.join(subdir, file)
      with open(dir_path, 'rb') as data:
        bucket.put_object(Key=dir_path[len(dir) + 1 :], Body=data)

        # Publish message to SNS.
        message_id = publish_message(
          'arn:aws:sns:us-east-1:973567983713:sns-s2030507',
          data,
          'Image upload status'
        )
        time.sleep(30)


def publish_message(topic_arn, message, subject):
    # Publishes a message to a topic.
    try:
      sns = boto3.client('sns', region_name='us-east-1')
      response = sns.publish(
          TopicArn=topic_arn,
          Message=str(message),
          Subject=subject,
      )['MessageId']

    except ClientError:
        logger.exception('ERROR: Couldn\'t publish message to the topic.')
        raise
    else:
        return response

upload_images('images')