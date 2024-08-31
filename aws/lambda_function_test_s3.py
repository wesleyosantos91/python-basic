from aws.src.s3 import S3Service

s3_service = S3Service()
s3_service.get_object_s3("person-v1", "registros.csv")


