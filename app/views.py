from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import base64
import boto3

# Initialize clients
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition', region_name='us-east-1')
dynamodb = boto3.client('dynamodb', region_name='us-east-1')

@csrf_exempt
def upload_and_recognize(request):
    try:
        if request.method == 'POST':
            # Ensure an image file is uploaded
            if 'image' not in request.FILES:
                return JsonResponse({'error': 'No image uploaded'}, status=400)

            # Get the image file from the POST request
            image_data = request.FILES['image']

            # Upload the image file to S3
            s3.upload_fileobj(image_data, 'imagesofpersonsfsd', 'uploaded_images/' + image_data.name)

            # Search for faces using Amazon Rekognition
            response = rekognition.search_faces_by_image(
                CollectionId="getdetails",
                Image={'S3Object': {'Bucket': 'imagesofpersonsfsd', 'Name': 'uploaded_images/' + image_data.name}}
            )

            # Prepare response data
            result = {'faces': []}
            if 'FaceMatches' in response:
                for match in response['FaceMatches']:
                    face_id = match['Face']['FaceId']
                    confidence = match['Face']['Confidence']

                    # Retrieve additional attributes from DynamoDB
                    face = dynamodb.get_item(
                        TableName='persondetails',
                        Key={'RekognitionId': {'S': face_id}}
                    )

                    if 'Item' in face:
                        item = face['Item']
                        face_data = {
                            'FaceId': face_id,
                            'Confidence': confidence,
                            'Details': {
                                'FName': item.get('fname', {}).get('S'),
                                'LName': item.get('lname', {}).get('S'),
                                'Gender': item.get('gender', {}).get('S'),
                                'DOB': item.get('dob', {}).get('S'),
                                'Email': item.get('email', {}).get('S'),
                                'Mobile': item.get('mobile', {}).get('S'),
                                'Address': item.get('address', {}).get('S'),
                                'Occupation': item.get('occupation', {}).get('S'),
                                'BloodGroup': item.get('bloodgroup', {}).get('S')
                            }
                        }

                        # Retrieve the corresponding image from S3
                        s3_response = s3.get_object(Bucket='imagesofpersonsfsd', Key='uploaded_images/' + image_data.name)

                        image_data = s3_response['Body'].read()
                        image_base64 = base64.b64encode(image_data).decode('utf-8')

                        face_data['Details']['Image'] = image_base64
                        result['faces'].append(face_data)

            # If no faces are found, return a message
            if not result['faces']:
                return JsonResponse({'message': 'No faces found'}, status=404)

            return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
