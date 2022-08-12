import json
import boto3

# Send SMS
def send_sms(event_body):
  sns = boto3.client('sns')
  phone_number = '+447722509271'
  message_content = str(event_body) + 'does not contain any PPE!'
  message_attributes = {
    'AWS.SNS.SMS.SMSType': {
        'DataType': 'String',
        'StringValue': 'Transactional',
    }
  }
  sns.publish(
    PhoneNumber=phone_number,
    Message=str(message_content),
    MessageAttributes=message_attributes
  )
  
def lambda_handler(event, context):
  s3 = boto3.resource('s3')
  table = boto3.resource('dynamodb').Table('S2030507_Image_Data')

  # Check the DynamoDB table is populated with all image data
  if len(table.scan()['Items']) == len(s3.Bucket('bucket-s2030507').objects.all()):
    print('All images have been uploaded to S3!')

    results = []
    for item in table.scan()['Items']:
      results.append(str(item['Image_Name']))

    event_body = event['Records'][0]['body']
    if event_body not in results:
      send_sms(event_body)
      print('SMS sent!' + '\n' + str(event_body) + ' does not contain any PPE!' + '\n')
    else:
          print(str(event_body) + ' contains PPE!' + '\n')
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }