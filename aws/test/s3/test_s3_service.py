import unittest
from unittest.mock import patch, MagicMock
from aws.src.s3.s3_service import S3Service

class TestS3Service(unittest.TestCase):

    @patch('boto3.client')
    @patch('aws_lambda_powertools.Logger')
    def test_get_object_s3_success(self, mock_logger, mock_boto_client):
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client
        mock_s3_client.head_object.return_value = {'ContentLength': 5 * 1024 * 1024}  # 5 MB
        mock_s3_client.download_file.return_value = None

        s3_service = S3Service()
        response = s3_service.get_object_s3('test-bucket', 'test-key')

        mock_s3_client.head_object.assert_called_once_with(Bucket='test-bucket', Key='test-key')
        mock_s3_client.download_file.assert_called_once_with(Bucket='test-bucket', Key='test-key', Filename='test-key')
        self.assertIsNone(response)

    @patch('boto3.client')
    @patch('aws_lambda_powertools.Logger')
    def test_get_object_s3_failure_due_to_size(self, mock_logger, mock_boto_client):
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client
        mock_s3_client.head_object.return_value = {'ContentLength': 15 * 1024 * 1024}  # 15 MB

        s3_service = S3Service()
        with self.assertRaises(Exception) as context:
            s3_service.get_object_s3('test-bucket', 'test-key')

        self.assertEqual(str(context.exception), "Object size is greater than 10MB")
        mock_s3_client.head_object.assert_called_once_with(Bucket='test-bucket', Key='test-key')
        mock_s3_client.download_file.assert_not_called()

    @patch('boto3.client')
    @patch('aws_lambda_powertools.Logger')
    def test_get_object_s3_failure_due_to_download_error(self, mock_logger, mock_boto_client):
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client
        mock_s3_client.head_object.return_value = {'ContentLength': 5 * 1024 * 1024}  # 5 MB
        mock_s3_client.download_file.side_effect = Exception('Error')

        s3_service = S3Service()
        with self.assertRaises(Exception):
            s3_service.get_object_s3('test-bucket', 'test-key')

        mock_s3_client.head_object.assert_called_once_with(Bucket='test-bucket', Key='test-key')
        mock_s3_client.download_file.assert_called_once_with(Bucket='test-bucket', Key='test-key', Filename='test-key')