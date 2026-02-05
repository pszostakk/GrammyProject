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

        health_fn = _lambda.Function(
            self, "HealthHandler",
            function_name=f"{PROJECT_NAME}-health-get-handler",
            runtime=_lambda.Runtime.PYTHON_3_14,
            handler="index.handler",
            code=_lambda.Code.from_asset(f"{BACKEND}/health/get"),
            timeout=Duration.seconds(10),
            memory_size=256
        )
        health_resource = base_api.root.add_resource("health")
        health_resource.add_method(
            "GET",
            apigateway.LambdaIntegration(
                health_fn,
                proxy=True
            ),
            api_key_required=False
        )

        pawel_fn = _lambda.Function(
            self, "PawelHandler",
            function_name=f"{PROJECT_NAME}-pawel-get-handler",
            runtime=_lambda.Runtime.PYTHON_3_14,
            handler="index.handler",
            code=_lambda.Code.from_asset(f"{BACKEND}/pawel/get"),
            timeout=_lambda.Duration.seconds(10),
            memory_size=256
        )
        pawel_resource = base_api.root.add_resource("pawel")
        pawel_resource.add_method(
            "GET",
            apigateway.LambdaIntegration(
                pawel_fn,
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

        