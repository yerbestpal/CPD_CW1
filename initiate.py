import boto3

def create_ec2_instance(instance_type, key_name):
  # Create EC2 Instance
  ec2 = boto3.resource('ec2')
  instances = ec2.create_instances(
    ImageId='ami-08e4e35cccc6189f4',
    MinCount=1,
    MaxCount=1,
    InstanceType=instance_type,
    KeyName=key_name,
    IamInstanceProfile={ 
      'Arn' : 'arn:aws:iam::973567983713:instance-profile/LabInstanceProfile'
    }
  )

  # Validate EC2 Instance
  if instances:
    print('EC2 Instance % s created' % instances[0].id)
  return

def create_sns_topic(topic_name):
  # Create SNS Topic
  sns = boto3.resource('sns')
  topic = sns.create_topic(Name=topic_name)

  # Validate SNS Topic
  if topic:
    print('SNS Topic % s created' % topic_name)
  return

def create_bucket(bucket_name, region_name):
  #  Create S3 Bucket
  session = boto3.Session(region_name=region_name)
  s3_client = session.client('s3')
  s3_client.create_bucket(Bucket=bucket_name)

  # Validate S3 Bucket
  buckets_list = s3_client.list_buckets()
  for bucket in buckets_list['Buckets']:
    if bucket['Name'] == 'bucket-s2030507':
      print('S3 Bucket created')
      break
    else:
      print('S3 Bucket not created')
      break
  return

create_ec2_instance('t2.micro', 'vockey')
create_sns_topic('sns-s2030507')
create_bucket('bucket-s2030507', 'us-east-1')