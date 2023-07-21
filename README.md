# click-and-upload-to-aws-s3
Often while working on AI-related Projects connected to images recognition, one of the common practices is to click the snapshot of the user and upload it to the cloud, so come up with a script to click the latest picture of the user, crop out only the face of the individual, remove the background, and upload the image to an S3 Bucket for further processing in AWS cloud, You have to do this from your local machine.

Expected Input: 
If the picture contains multiple people, separate images of all the individuals should be uploaded.
 For example, If my webcam takes this picture
2.Pictures should be uploaded to S3 bucket to AWS cloud


Expected Output: 
Once I run the script, the system takes the latest photo of the user from the webcam and uploads the image to S3 bucket for further processing.
 
