import os
import unittest
from unittest.mock import patch, MagicMock

from aws.src.sqs.sqs_service import SQSService


class TestSQSService(unittest.TestCase):

    @patch.dict(os.environ, {"ENVIROMENT": "local", "SQS_ENDPOINT": "http://localhost:4566/queue/test"})
    @patch('boto3.client')
    def test_send_messages_local(self, mock_boto_client):
        # Arrange
        mock_sqs_client = MagicMock()
        mock_boto_client.return_value = mock_sqs_client
        sqs_service = SQSService()
        messages = [
            {'Id': '1', 'MessageBody': 'message 1'},
            {'Id': '2', 'MessageBody': 'message 2'}
        ]

        # Act
        sqs_service.send_messages(messages)

        # Assert
        mock_sqs_client.send_message_batch.assert_called_once_with(
            QueueUrl="http://localhost:4566/queue/test",
            Entries=messages
        )

    @patch.dict(os.environ, {"ENVIROMENT": "production", "SQS_ENDPOINT": "https://sqs.us-east-1.amazonaws.com/123456789012/test"})
    @patch('boto3.client')
    def test_send_messages_production(self, mock_boto_client):
        # Arrange
        mock_sqs_client = MagicMock()
        mock_boto_client.return_value = mock_sqs_client
        sqs_service = SQSService()
        messages = [
            {'Id': '1', 'MessageBody': 'message 1'},
            {'Id': '2', 'MessageBody': 'message 2'}
        ]

        # Act
        sqs_service.send_messages(messages)

        # Assert
        mock_sqs_client.send_message_batch.assert_called_once_with(
            QueueUrl="https://sqs.us-east-1.amazonaws.com/123456789012/test",
            Entries=messages
        )

