import unittest
from unittest.mock import patch, MagicMock
from aws.src.core.handler_service import HandlerService

class TestHandlerService(unittest.TestCase):

    @patch('aws.src.core.handler_service.uuid.uuid4')
    @patch('aws.src.core.handler_service.duckdb.connect')
    @patch('aws.src.core.handler_service.S3Service')
    @patch('aws.src.core.handler_service.SQSService')
    @patch('aws.src.core.handler_service.Logger')
    def test_handles_event_successfully(self, mock_logger, mock_sqs_service, mock_s3_service, mock_duckdb_connect, mock_uuid):
        mock_logger_instance = MagicMock()
        mock_logger.return_value = mock_logger_instance
        mock_s3_service_instance = MagicMock()
        mock_s3_service.return_value = mock_s3_service_instance
        mock_sqs_service_instance = MagicMock()
        mock_sqs_service.return_value = mock_sqs_service_instance
        mock_duckdb_connection = MagicMock()
        mock_duckdb_connect.return_value = mock_duckdb_connection
        mock_uuid.return_value = '1234'

        mock_duckdb_connection.read_csv.return_value.fetchdf.return_value.iterrows.return_value = [
            (0, MagicMock(to_json=MagicMock(return_value='{"key": "value"}')))
        ]

        handler_service = HandlerService()
        event = {'Records': [{'s3': {'bucket': {'name': 'test-bucket'}, 'object': {'key': 'test-key'}}}]}
        context = {}

        handler_service.handler_process(event, context)

        mock_s3_service_instance.get_object_s3.assert_called_once_with('test-bucket', 'test-key')
        mock_sqs_service_instance.send_messages.assert_called_once_with([{'Id': '1234', 'MessageBody': '{"key": "value"}'}])
        mock_logger_instance.info.assert_called()

    @patch('aws.src.core.handler_service.uuid.uuid4')
    @patch('aws.src.core.handler_service.duckdb.connect')
    @patch('aws.src.core.handler_service.S3Service')
    @patch('aws.src.core.handler_service.SQSService')
    @patch('aws.src.core.handler_service.Logger')
    def test_handles_event_with_multiple_batches(self, mock_logger, mock_sqs_service, mock_s3_service, mock_duckdb_connect, mock_uuid):
        mock_logger_instance = MagicMock()
        mock_logger.return_value = mock_logger_instance
        mock_s3_service_instance = MagicMock()
        mock_s3_service.return_value = mock_s3_service_instance
        mock_sqs_service_instance = MagicMock()
        mock_sqs_service.return_value = mock_sqs_service_instance
        mock_duckdb_connection = MagicMock()
        mock_duckdb_connect.return_value = mock_duckdb_connection
        mock_uuid.side_effect = [str(i) for i in range(20)]

        mock_duckdb_connection.read_csv.return_value.fetchdf.return_value.iterrows.return_value = [
            (i, MagicMock(to_json=MagicMock(return_value=f'{{"key": "value{i}"}}'))) for i in range(20)
        ]

        handler_service = HandlerService()
        event = {'Records': [{'s3': {'bucket': {'name': 'test-bucket'}, 'object': {'key': 'test-key'}}}]}
        context = {}

        handler_service.handler_process(event, context)

        self.assertEqual(mock_sqs_service_instance.send_messages.call_count, 2)
        mock_logger_instance.info.assert_called()

    @patch('aws.src.core.handler_service.uuid.uuid4')
    @patch('aws.src.core.handler_service.duckdb.connect')
    @patch('aws.src.core.handler_service.S3Service')
    @patch('aws.src.core.handler_service.SQSService')
    @patch('aws.src.core.handler_service.Logger')
    def test_handles_event_with_empty_dataframe(self, mock_logger, mock_sqs_service, mock_s3_service, mock_duckdb_connect, mock_uuid):
        mock_logger_instance = MagicMock()
        mock_logger.return_value = mock_logger_instance
        mock_s3_service_instance = MagicMock()
        mock_s3_service.return_value = mock_s3_service_instance
        mock_sqs_service_instance = MagicMock()
        mock_sqs_service.return_value = mock_sqs_service_instance
        mock_duckdb_connection = MagicMock()
        mock_duckdb_connect.return_value = mock_duckdb_connection

        mock_duckdb_connection.read_csv.return_value.fetchdf.return_value.iterrows.return_value = []

        handler_service = HandlerService()
        event = {'Records': [{'s3': {'bucket': {'name': 'test-bucket'}, 'object': {'key': 'test-key'}}}]}
        context = {}

        handler_service.handler_process(event, context)

        mock_s3_service_instance.get_object_s3.assert_called_once_with('test-bucket', 'test-key')
        mock_sqs_service_instance.send_messages.assert_not_called()
        mock_logger_instance.info.assert_called()