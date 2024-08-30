import os

import boto3
from aws_lambda_powertools import Logger

env = os.getenv("ENVIROMENT")

class S3Service:

    def __init__(self):
        if env == "local":
            self.__s3_client = boto3.client('s3', endpoint_url='https://localhost.localstack.cloud:4566')
        else:
            self.__s3_client = boto3.client('s3')
        self.__logger = Logger(service="S3Service")

    def get_object_s3(self, bucket, key):
        try:
            self.__logger.info(f"Getting object from bucket {bucket} with key {key}")
            response = self.__s3_client.download_file(Bucket=bucket, Key=key, Filename=f"{key}")
            self.__logger.info(f"Object from bucket {bucket} with key {key} retrieved")
            return response
        except Exception as erro:
            self.__logger.error(f"Error getting object from bucket {bucket} with key {key}")
            raise erro