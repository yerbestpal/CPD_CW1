import json
import boto3

# Send SMS
def send_sms():
  sns = boto3.client('sns')
  phone_number = '+44- 7722509271'
  message_content = 'Message successful!'
  message_attributes = {
    "AWS.SNS.SMS.SMSType": {
        'DataType': 'String',
        'StringValue': 'Transactional',
    }
  }
  sns.publish(
    PhoneNumber=phone_number,
    Message=str(message_content),
    MessageAttributes=message_attributes,
  )
  
# Call function
send_sms()