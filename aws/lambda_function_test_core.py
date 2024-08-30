from aws.core.handler_service import HandlerService

event = {
    "Records": [
        {
            "s3": {
                "bucket": {
                    "name": "person-v1"
                },
                "object": {
                    "key": "registros.csv"
                }
            }
        }
    ]
}

handler_core = HandlerService()

handler_core.handler_process(event, None)