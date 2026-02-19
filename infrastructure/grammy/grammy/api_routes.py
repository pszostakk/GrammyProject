"""API Gateway route definitions and builders."""
from typing import NamedTuple, List, Optional
from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_lambda as _lambda


class RouteConfig(NamedTuple):
    """Configuration for an API Gateway route."""
    path: str
    method: str
    lambda_function: _lambda.Function
    api_key_required: bool = False
    auth_required: bool = True  # NEW


def _get_or_create_resource(root: apigateway.IResource, path: str) -> apigateway.IResource:
    clean = path.strip("/")
    if not clean:
        return root

    current = root
    for part in clean.split("/"):
        current = current.get_resource(part) or current.add_resource(part)
    return current


def create_api_routes(
    base_api: apigateway.RestApi,
    routes: List[RouteConfig],
    authorizer: Optional[apigateway.IAuthorizer] = None,
) -> None:
    """Create API Gateway routes from configuration."""
    for route in routes:
        resource = _get_or_create_resource(base_api.root, route.path)

        integration = apigateway.LambdaIntegration(
            route.lambda_function,
            proxy=True,
        )

        # CDK 2.1012: ustawienia przekazujemy jako keyword args, bez MethodOptions/options=
        if authorizer and route.auth_required:
            resource.add_method(
                route.method,
                integration,
                api_key_required=route.api_key_required,
                authorization_type=apigateway.AuthorizationType.COGNITO,
                authorizer=authorizer,
            )
        else:
            resource.add_method(
                route.method,
                integration,
                api_key_required=route.api_key_required,
                authorization_type=apigateway.AuthorizationType.NONE,
            )
