import unittest
from unittest.mock import patch, MagicMock
from aws.src.s3.s3_service import S3Service

class TestS3Service(unittest.TestCase):

    @patch('boto3.client')
    @patch('aws_lambda_powertools.Logger')
    def test_get_object_s3_success(self, mock_logger, mock_boto_client):
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client
        mock_s3_client.download_file.return_value = None

        s3_service = S3Service()
        response = s3_service.get_object_s3('test-bucket', 'test-key')

        mock_s3_client.download_file.assert_called_once_with(Bucket='test-bucket', Key='test-key', Filename='test-key')
        self.assertIsNone(response)

    @patch('boto3.client')
    @patch('aws_lambda_powertools.Logger')
    def test_get_object_s3_failure(self, mock_logger, mock_boto_client):
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client
        mock_s3_client.download_file.side_effect = Exception('Error')

        s3_service = S3Service()
        with self.assertRaises(Exception):
            s3_service.get_object_s3('test-bucket', 'test-key')

        mock_s3_client.download_file.assert_called_once_with(Bucket='test-bucket', Key='test-key', Filename='test-key')