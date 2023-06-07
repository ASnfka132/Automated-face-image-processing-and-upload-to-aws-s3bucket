import cv2
import numpy as np
import boto3
import os
from rembg import remove
from PIL import Image

# Set up AWS credentials
AWS_ACCESS_KEY_ID = 'Your-Access-key'
AWS_SECRET_ACCESS_KEY = 'Your-AWS-Secret-Access_Key'
AWS_REGION = 'us-east-1'
S3_BUCKET_NAME = 'bucket-name'

# Initialize the AWS S3 client
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                         region_name=AWS_REGION)

# Capture the latest image from the webcam
def capture_image():
    capture = cv2.VideoCapture(0)
    ret, frame = capture.read()
    cv2.imwrite('captured_image.jpg', frame)
    capture.release()

# Remove the background from the image using rembg
def remove_background(image_path):
    input_img = cv2.imread(image_path)
    input_img_rgb = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(input_img_rgb)
    output_img = remove(pil_image)
    output_img_rgb = output_img.convert("RGB")
    output_img_bgr = cv2.cvtColor(np.array(output_img_rgb), cv2.COLOR_RGB2BGR)
    output_path = 'processed_image.png'
    cv2.imwrite(output_path, output_img_bgr)
    return output_path

# Upload the image to the S3 bucket
def upload_image(image_path, file_name):
    s3_client.upload_file(image_path, S3_BUCKET_NAME, file_name)

# Split the image into separate images of individual persons
def split_image(image_path):
    input_img = cv2.imread(image_path)
    gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    cascade_path =cascade_path = r" "  # Update the path if necessary
    face_cascade = cv2.CascadeClassifier(cascade_path)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    image_paths = []
    for (x, y, w, h) in faces:
        face_img = input_img[y:y+h, x:x+w]
        face_path = f"face_{x}_{y}.png"
        cv2.imwrite(face_path, face_img)
        image_paths.append(face_path)
    
    return image_paths

# Main function
def main():
    capture_image()
    processed_image_path = remove_background('captured_image.jpg')
    individual_image_paths = split_image(processed_image_path)

    for image_path in individual_image_paths:
        file_name = os.path.basename(image_path)
        upload_image(image_path, file_name)

    # Clean up the local files
    #os.remove('captured_image.jpg')
    #os.remove('processed_image.png')
    #for image_path in individual_image_paths:
    #   os.remove(image_path)

if __name__ == '__main__':
    main()