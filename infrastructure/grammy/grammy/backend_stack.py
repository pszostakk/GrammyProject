"""Backend Stack - Lambda, API Gateway, Cognito, IAM"""
from aws_cdk import (
    Stack,
    CfnOutput,
    RemovalPolicy,
    Duration,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_cognito as cognito,
    aws_iam as iam,
)
from constructs import Construct
from .config import PROJECT_NAME, HANDLERS, ROUTES, CLOUDFRONT_DOMAIN
from .handlers import create_lambda_function
from .api_routes import create_api_routes, RouteConfig


class BackendStack(Stack):
    """Stack for backend resources: Lambda, API Gateway, Cognito."""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        table_name: str,
        table_arn: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.table_name = table_name
        self.table_arn = table_arn

        # ───────────── Cognito User Pool ─────────────
        self.user_pool = cognito.UserPool(
            self,
            f"{PROJECT_NAME}-user-pool",
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(email=True),
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
            mfa=cognito.Mfa.REQUIRED,
            mfa_second_factor=cognito.MfaSecondFactor(sms=False, otp=True),
            removal_policy=RemovalPolicy.DESTROY,
        )

        self.user_pool_client = self.user_pool.add_client(
            f"{PROJECT_NAME}-app-client",
            auth_flows=cognito.AuthFlow(
                user_srp=True,
                user_password=True,
                admin_user_password=True,
            ),
            id_token_validity=Duration.hours(1),
            access_token_validity=Duration.hours(1),
            refresh_token_validity=Duration.hours(1),
            enable_token_revocation=True,
        )

        # ───────────── API Gateway ─────────────
        self.base_api = self._create_api_gateway()

        # ───────────── Lambda functions ─────────────
        self.lambda_functions = self._create_lambda_functions()

        # ───────────── Cognito Authorizer ─────────────
        self.authorizer = apigateway.CognitoUserPoolsAuthorizer(
            self.base_api,
            f"{PROJECT_NAME}-authorizer",
            cognito_user_pools=[self.user_pool],
            identity_source="method.request.header.Authorization",
        )

        # ───────────── API Routes ─────────────
        self._create_routes(self.base_api, self.lambda_functions, self.authorizer)

        # ───────────── Outputs ─────────────
        CfnOutput(
            self,
            "UserPoolId",
            value=self.user_pool.user_pool_id,
            export_name=f"{PROJECT_NAME}-user-pool-id",
        )
        CfnOutput(
            self,
            "UserPoolClientId",
            value=self.user_pool_client.user_pool_client_id,
            export_name=f"{PROJECT_NAME}-user-pool-client-id",
        )
        CfnOutput(
            self,
            "ApiUrl",
            value=self.base_api.url,
            export_name=f"{PROJECT_NAME}-api-url",
        )

    def _create_api_gateway(self) -> apigateway.RestApi:
        """Create and configure API Gateway."""
        return apigateway.RestApi(
            self,
            f"{PROJECT_NAME}-base-api",
            rest_api_name=f"{PROJECT_NAME} Base API",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=[
                    f"https://{CLOUDFRONT_DOMAIN}",
                    "http://localhost:5173"
                ],
                allow_methods=apigateway.Cors.ALL_METHODS,
                allow_headers=[
                    "Content-Type",
                    "Authorization",
                ],
            ),
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
            if fn.log_group:
                fn.log_group.apply_removal_policy(RemovalPolicy.DESTROY)
            
            # Grant DynamoDB access
            fn.add_environment("TABLE_NAME", self.table_name)
            fn.add_to_role_policy(
                iam.PolicyStatement(
                    actions=[
                        "dynamodb:GetItem",
                        "dynamodb:PutItem",
                        "dynamodb:UpdateItem",
                        "dynamodb:DeleteItem",
                        "dynamodb:Query",
                        "dynamodb:Scan",
                    ],
                    resources=[self.table_arn],
                )
            )
            
            lambda_functions[handler_config.name] = fn
        return lambda_functions

    def _create_routes(
        self,
        base_api: apigateway.RestApi,
        lambda_functions: dict,
        authorizer: apigateway.CognitoUserPoolsAuthorizer,
    ) -> None:
        """Create API routes."""
        routes = [
            RouteConfig(
                path=route_def["path"],
                method=route_def.get("method", "GET"),
                lambda_function=lambda_functions[route_def["handler"]],
                api_key_required=route_def.get("api_key_required", False),
                auth_required=route_def.get("auth_required", True),
            )
            for route_def in ROUTES
        ]
        create_api_routes(base_api, routes, authorizer=authorizer)
