import json
import boto3

# Send SMS
def send_sms(msg, number):
  sns = boto3.client('sns')
  message_attributes = {
    "AWS.SNS.SMS.SMSType": {
        'DataType': 'String',
        'StringValue': 'Transactional',
    }
  }
  sns.publish(
    PhoneNumber=number,
    Message=str(msg),
    MessageAttributes=message_attributes,
  )