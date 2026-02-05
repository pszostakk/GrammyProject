from aws_cdk import (
    Stack,
    aws_lambda as _lambda
)
from constructs import Construct

class GrammyStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Simple Hello World Lambda function
        hello_fn = _lambda.Function(
            self, "HelloHandler",
            runtime=_lambda.Runtime.PYTHON_3_14,
            handler="index.handler",
            code=_lambda.Code.from_inline(
                "def handler(event, context):\n    return {'statusCode': 200, 'body': 'Hello, World!'}"
            ),
        )
