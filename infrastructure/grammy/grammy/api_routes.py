"""API Gateway route definitions and builders."""
from typing import NamedTuple, List
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_lambda as _lambda


class RouteConfig(NamedTuple):
    """Configuration for an API Gateway route."""
    path: str
    method: str
    lambda_function: _lambda.Function
    api_key_required: bool = False


def create_api_routes(
    base_api: apigateway.RestApi,
    routes: List[RouteConfig]
) -> None:
    """Create API Gateway routes from configuration.
    
    Args:
        base_api: API Gateway RestApi instance
        routes: List of RouteConfig definitions
    """
    for route in routes:
        resource = base_api.root.add_resource(route.path)
        resource.add_method(
            route.method,
            apigateway.LambdaIntegration(
                route.lambda_function,
                proxy=True
            ),
            api_key_required=route.api_key_required,
        )
