import io
import uuid

import duckdb
from aws_lambda_powertools import Logger

from aws.s3.s3_service import S3Service
from aws.sqs.sqs_service import SQSService

MAX_MESSAGES = 10

class HandlerService:

    def __init__(self):
        self.__logger = Logger(service="HandlerService")
        self.__s3_service = S3Service()
        self.__sqs_service = SQSService()
        self.__duckdb_connection = duckdb.connect(database=':memory:', read_only=False)

    def handler_process(self, event, context):
        self.__logger.info(f"Initializing handling of event: {event}")
        self.__logger.info(f"Initializing handling of contetxt: {context}")

        bucket = str(event['Records'][0]['s3']['bucket']['name'])
        key = str(event['Records'][0]['s3']['object']['key'])

        self.__s3_service.get_object_s3(bucket, key)

        df = self.__duckdb_connection.read_csv(f'.\\{key}', header=True, sep=';')

        messages = []

        for index, row in df.iterrows():
            messages.append({'Id': str(uuid.uuid4()), 'MessageBody': row.to_json()})

            if len(messages) == MAX_MESSAGES:
                self.__sqs_service.send_messages(messages)
                messages = []

        if len(messages) > 0:
            self.__sqs_service.send_messages(messages)

        self.__logger.info("Event handled successfully")

