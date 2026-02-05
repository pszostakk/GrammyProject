from aws_cdk import (
    Stack,
    CfnOutput,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
)
from constructs import Construct
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND = PROJECT_ROOT / "backend"
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
            timeout=_lambda.Duration.seconds(10),
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

        CfnOutput(
            self,
            "ApiUrl",
            value=base_api.url,
            description="Grammy API URL"
        )