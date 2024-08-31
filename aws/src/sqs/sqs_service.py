import os

import boto3
from aws_lambda_powertools import Logger

env = os.getenv("ENVIROMENT")

class SQSService:

    def __init__(self):
        if env == "local":
            self.__sqs_client = boto3.client('sqs', endpoint_url='https://localhost.localstack.cloud:4566')
        else:
            self.__sqs_client = boto3.client('sqs')
        self.__sqs_endpoint = os.getenv('SQS_ENDPOINT')
        self.__logeer = Logger(service="SQSService")

    def send_messages(self, messages):
        self.__logeer.info(f"Sending messages to queue {self.__sqs_endpoint}")

        self.__sqs_client.send_message_batch(
            QueueUrl=self.__sqs_endpoint,
            Entries=messages
        )
        self.__logeer.info("Messages sent to SQS")
