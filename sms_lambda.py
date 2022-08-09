import json
import boto3

# Send SMS
def send_sms():
  sns = boto3.client('sns')
  phone_number = '+447722509271'
  message_content = 'Message successful!'
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
  # Call function
  print("It worked!")
  send_sms(event, context)
  return {
      'statusCode': 200,
      'body': json.dumps(str(event['Records'][0]))
  }