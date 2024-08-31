from aws.src.sqs.sqs_service import SQSService

sqs_service = SQSService()
messages = [{'Id': '1', 'MessageBody': 'Hello'}, {'Id': '2', 'MessageBody': 'World'}]
sqs_service.send_messages(messages)


