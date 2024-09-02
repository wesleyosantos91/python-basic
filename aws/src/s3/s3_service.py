import os

import boto3
from aws_lambda_powertools import Logger

env = os.getenv("ENVIRONMENT")
BYTES_PER_MB = 1024 * 1024
TEN_MB_IN_BYTES = 10 * BYTES_PER_MB


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

            head_response = self.__s3_client.head_object(Bucket=bucket, Key=key)

            object_size = head_response['ContentLength']

            if object_size > TEN_MB_IN_BYTES:
                raise Exception("Object size is greater than 10MB")

            response = self.__s3_client.download_file(Bucket=bucket, Key=key, Filename=key)
            self.__logger.info(f"Object from bucket {bucket} with key {key} retrieved")
            return response
        except Exception as erro:
            self.__logger.error(f"Error getting object from bucket {bucket} with key {key}")
            raise erro