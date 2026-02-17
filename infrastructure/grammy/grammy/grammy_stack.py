from aws_cdk import (
    RemovalPolicy,
    Stack,
    CfnOutput,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_s3_deployment as s3deploy,
    aws_iam as iam,
)
from constructs import Construct
from .config import PROJECT_NAME, HANDLERS, ROUTES
from .handlers import create_lambda_function
from .api_routes import create_api_routes, RouteConfig


class GrammyStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        website_bucket = s3.Bucket(
            self,
            "FrontendBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        )

        oac = cloudfront.CfnOriginAccessControl(
            self,
            "FrontendOAC",
            origin_access_control_config=cloudfront.CfnOriginAccessControl.OriginAccessControlConfigProperty(
                name="frontend-oac",
                origin_access_control_origin_type="s3",
                signing_behavior="always",
                signing_protocol="sigv4",
            ),
        )

        distribution = cloudfront.CfnDistribution(
            self,
            "FrontendDistribution",
            distribution_config=cloudfront.CfnDistribution.DistributionConfigProperty(
                enabled=True,
                default_root_object="index.html",
                origins=[
                    cloudfront.CfnDistribution.OriginProperty(
                        id="S3Origin",
                        domain_name=website_bucket.bucket_regional_domain_name,
                        origin_access_control_id=oac.ref,
                        s3_origin_config=cloudfront.CfnDistribution.S3OriginConfigProperty(
                            origin_access_identity=""
                        ),
                    )
                ],
                default_cache_behavior=cloudfront.CfnDistribution.DefaultCacheBehaviorProperty(
                    target_origin_id="S3Origin",
                    viewer_protocol_policy="redirect-to-https",
                    allowed_methods=["GET", "HEAD", "OPTIONS"],
                    cached_methods=["GET", "HEAD"],
                    compress=True,
                    forwarded_values=cloudfront.CfnDistribution.ForwardedValuesProperty(
                        query_string=False,
                        cookies=cloudfront.CfnDistribution.CookiesProperty(forward="none"),
                    ),
                ),
            ),
        )

        website_bucket.add_to_resource_policy(
            iam.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[website_bucket.arn_for_objects("*")],
                principals=[iam.ServicePrincipal("cloudfront.amazonaws.com")],
                conditions={
                    "StringEquals": {
                        "AWS:SourceArn": f"arn:aws:cloudfront::{self.account}:distribution/{distribution.ref}"
                    }
                },
            )
        )

        s3deploy.BucketDeployment(
            self,
            "DeployFrontend",
            sources=[s3deploy.Source.asset("../../frontend/dist")],
            destination_bucket=website_bucket,
        )

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

        # Outputs
        CfnOutput(self, "ApiUrl", value=base_api.url)
        CfnOutput(self, "FrontendUrl", value=f"https://{distribution.attr_domain_name}")
        CfnOutput(self, "FrontendBucketName", value=website_bucket.bucket_name)


    def _create_api_gateway(self) -> apigateway.RestApi:
        """Create and configure API Gateway."""
        return apigateway.RestApi(
            self,
            f"{PROJECT_NAME}-base-api",
            rest_api_name=f"{PROJECT_NAME} Base API",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=[
                    "https://d1ha3xi7so3sx5.cloudfront.net",
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
