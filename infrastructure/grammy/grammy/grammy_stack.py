from aws_cdk import (
    Stack,
    CfnOutput,
    Duration,
    aws_lambda as _lambda,
    aws_apigateway as apigateway
)
from constructs import Construct

PROJECT_ROOT = "../../"
BACKEND = f"{PROJECT_ROOT}backend"
PROJECT_NAME = "grammy"

class GrammyStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        base_api = apigateway.RestApi(
            self,
            f"{PROJECT_NAME}-base-api",
            rest_api_name=f"{PROJECT_NAME} Base API",
            deploy_options=apigateway.StageOptions(
                stage_name="dev",
                logging_level=apigateway.MethodLoggingLevel.INFO,
                metrics_enabled=True,
                data_trace_enabled=True,
            ),
        )

        kacper_fn = _lambda.Function(
            self, "KacperHandler",
            function_name=f"{PROJECT_NAME}-kacper-get-handler",
            runtime=_lambda.Runtime.PYTHON_3_14,
            handler="index.handler",
            code=_lambda.Code.from_asset(f"{BACKEND}/kacper/get"),
            timeout=Duration.seconds(10),
            memory_size=256
        )
        kacper_resource = base_api.root.add_resource("kacper")
        kacper_resource.add_method(
            "GET",
            apigateway.LambdaIntegration(
                kacper_fn,
                proxy=True
            ),
            api_key_required=False
        )

        CfnOutput(
            self,
            "ApiUrl",
            value=base_api.url,
            description="Grammy API URL"
        )
