import json
from urllib import response
import boto3

def lambda_handler(event, context):
  s3_client = boto3.client('s3')
  client = boto3.client('rekognition')

  for msg in event['Records']:
    msg_payload = json.loads(msg['body'])

    if 'Records' in msg_payload:
      bucket = msg_payload['Records'][0]['s3']['bucket']['name']
      image = msg_payload['Records'][0]['s3']['object']['key'].replace('+', ' ')
      response = client.detect_protective_equipment(
        Image={
          'S3Object': {
            'Bucket': bucket,
            'Name': image
          }
        },
        SummarizationAttributes={
          'MinConfidence': 80,
          'RequiredEquipmentTypes': [
            'FACE_COVER',
            'HEAD_COVER'
          ]
        }
      )

      results = []

      for person in response['Persons']:
        body_parts = person['BodyParts']
        result = {
          'Image_Name': image,
          'Details': []
        }

        for equipment_detections in body_parts:
          name = equipment_detections['Name']
          ppe = equipment_detections['EquipmentDetections']
          for ppe_type in ppe:
            types = ppe_type['Type']
            confidence = ppe_type['Confidence']
            covers_body = ppe_type['CoversBodyPart']['Value']

            person_details = {
              'Body Part': name,
              'Confidence': confidence,
              'Cover Type': types,
              'Covers Body Part': covers_body
            }

          result['Details'].append(person_details)
        
        if len(result['Details']) > 0:
          results.append(result)

        table = boto3.resource('dynamodb').Table('S2030507_Image_Data')
        table.put_item(
          Item={
            'Image_Name': image,
            'Labels': result
          }
        )