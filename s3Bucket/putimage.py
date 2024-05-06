import boto3

# Initialize S3 client
s3 = boto3.resource('s3')

# List of images with corresponding metadata
images = [
    ('tovino.jpg', 'tovino', 'kk','female','20-10-1999','b+ve',  'example@example.com', '9080988','Occupaho', 'business'),
    ('jayasurya.jpg', 'jayasurya', 'k','male','20-10-1999','b+ve',  'example@example.com', '9080988','Occupaho', 'business'),
    ('naslen.jpg', 'naslen', 'k','male','20-10-1999','b+ve',  'example@example.com', '9080988','Occupaho', 'business'),
    ('mamitha.jpg', 'mamitha', 'k','male','20-10-1999','b+ve',  'example@example.com', '9080988','Occupaho', 'business'),
    ('Anaswara.jpg', 'Anaswara', 'k','male','20-10-1999','b+ve',  'example@example.com', '9080988','Occupaho', 'business'),
]

# Upload images to S3 with metadata
for image in images:
    try:
        with open(image[0], 'rb') as file:
            # Use put_object method directly for simplicity
            s3.meta.client.put_object(
                Bucket='imagesofpersonsfsd',
                Key='images/' + image[0],
                Body=file,
                Metadata={
                    'fname': image[1],
                    'lname': image[2],
                    'gender': image[3],
                    'dob': image[4],
                    'bloodgroup': image[5],
                    'email': image[6],
                    'mobile': image[7],
                    'address': image[8],
                    'occupation': image[9]
                }
            )
            print("Uploaded:", image[0])
    except FileNotFoundError as e:
        print("Error: File not found -", e)
    except Exception as e:
        print("Error uploading", image[0], ":", e)