from aws.s3.s3_service import S3Service

s3_service = S3Service()
s3_service.get_object_s3("person-v1", "registros.csv")


