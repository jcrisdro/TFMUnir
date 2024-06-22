import os
import boto3
import base64


from constants import AWS, ROOT_PROJECT

class AWSClient:

    def __init__(self) -> None:
        self.boto_client = None

    def client(self, resource: str = 's3'):
        if self.boto_client is None:
            self.boto_client = boto3.client(
                resource,
                aws_access_key_id=AWS['AWS_ACCESS_KEY'],
                aws_secret_access_key=AWS['AWS_SECRET_ACCESS'],
                region_name=AWS['AWS_REGION']
            )
        return self.boto_client

    def get_video(self, file_object: str = None) -> str:
        """ Get video from S3 bucket """
        try:
            s3 = self.client('s3')
            s3.download_file(Bucket=AWS['AWS_BUCKET'], Key=file_object, Filename=file_object)
            return f'{ROOT_PROJECT}/{file_object}'
        except Exception as e:
            print(f"Exception: {e}")
            return None
