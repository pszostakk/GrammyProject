from aws_cdk import (
    RemovalPolicy,
    Stack,
    CfnOutput,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb
)
from constructs import Construct
from .config import PROJECT_NAME, HANDLERS, ROUTES
from .handlers import create_lambda_function
from .api_routes import create_api_routes, RouteConfig


class GrammyStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create API Gateway
        base_api = self._create_api_gateway()

        # Create Lambda functions
        lambda_functions = self._create_lambda_functions()

        # Create DynamoDB table with read/write permissions for all Lambdas
        table = self._create_dynamodb_table()
        for fn in lambda_functions.values():
            fn.add_environment("TABLE_NAME", table.table_name)
            table.grant_read_write_data(fn)

        # Create API routes
        self._create_routes(base_api, lambda_functions)

        # Output API URL
        CfnOutput(
            self,
            "ApiUrl",
            value=base_api.url,
            description="Grammy API URL"
        )

    def _create_api_gateway(self) -> apigateway.RestApi:
        """Create and configure API Gateway."""
        return apigateway.RestApi(
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

    def _create_lambda_functions(self) -> dict:
        """Create all Lambda functions and return mapping by name."""
        lambda_functions = {}
        for handler_config in HANDLERS:
            fn = create_lambda_function(self, handler_config, PROJECT_NAME)
            lambda_functions[handler_config.name] = fn
        return lambda_functions
    
    def _create_dynamodb_table(self) -> dynamodb.Table:
     return dynamodb.Table(
        self,
        "GrammyTable",
        table_name=f"{PROJECT_NAME}-table",
        partition_key=dynamodb.Attribute(
            name="PK",
            type=dynamodb.AttributeType.STRING
        ),
        sort_key=dynamodb.Attribute(
            name="SK",
            type=dynamodb.AttributeType.STRING
        ),
        #billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST, - to discuss with Jakub
        #removal_policy=RemovalPolicy.DESTROY - to discuss with Jakub
    )

    def _create_routes(
        self,
        base_api: apigateway.RestApi,
        lambda_functions: dict
    ) -> None:
        """Create API routes."""
        routes = [
            RouteConfig(
                path=route_def["path"],
                method=route_def.get("method", "GET"),
                lambda_function=lambda_functions[route_def["handler"]],
                api_key_required=route_def.get("api_key_required", False),
            )
            for route_def in ROUTES
        ]
        create_api_routes(base_api, routes)
