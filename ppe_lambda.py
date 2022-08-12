import json
import boto3
from decimal import Decimal

def lambda_handler(event, context):
  s3_client = boto3.client('s3')
  client = boto3.client('rekognition', region_name='us-east-1')

  # Loop Records
  for msg in event['Records']:
    print(msg)

    bucket = 'bucket-s2030507'
    image = str(msg['body'])

    # Detect faces and hands in image
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
              'HAND_COVER'
          ]
      }
    )

    results = []

    # Loop individuals in results
    for person in response['Persons']:
      body_parts = person['BodyParts']
      result = {
        'Image_Name': image,
        'Details': []
      }

      # Loop body parts to gain details
      for body_part in body_parts:
        name = body_part['Name']

        person_details = {
          'Body Part': name,
        }

        # Check if body part has PPE and add the relevant details to the result
        ppe = body_part['EquipmentDetections']
        for ppe_type in ppe:
          types = ppe_type['Type']
          confidence = ppe_type['Confidence']
          covers_body = ppe_type['CoversBodyPart']['Value']

          person_details['Confidence'] = confidence
          person_details['Cover Type'] = types
          person_details['Covers Body Part'] = covers_body

        result['Details'].append(person_details)
        results.append(result)

        # Build item from results
        item = json.loads(json.dumps({
          'Image_Name': image,
          'Labels': result
        }), parse_float=Decimal)

        # Upload item to S3
        table = boto3.resource('dynamodb').Table('S2030507_Image_Data')
        table.put_item(Item=item)