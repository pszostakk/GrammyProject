"""Frontend Stack - S3 static site, CloudFront, OAC, ACM"""
from aws_cdk import (
    Stack,
    CfnOutput,
    RemovalPolicy,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_certificatemanager as acm,
)
from constructs import Construct
import json
from .config import PROJECT_NAME


class FrontendStack(Stack):
    """Stack for frontend resources: S3, CloudFront, OAC, ACM."""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        api_url: str,
        user_pool_id: str,
        user_pool_client_id: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ───────────── Frontend: S3 bucket ─────────────
        self.website_bucket = s3.Bucket(
            self,
            "FrontendBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        )

        # ───────────── Frontend: CloudFront OAC ─────────────
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

        # ───────────── Frontend: CloudFront Distribution ─────────────
        self.distribution = cloudfront.CfnDistribution(
            self,
            "FrontendDistribution",
            distribution_config=cloudfront.CfnDistribution.DistributionConfigProperty(
                enabled=True,
                default_root_object="index.html",
                origins=[
                    cloudfront.CfnDistribution.OriginProperty(
                        id="S3Origin",
                        domain_name=self.website_bucket.bucket_regional_domain_name,
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
                custom_error_responses=[
                    cloudfront.CfnDistribution.CustomErrorResponseProperty(
                        error_code=403,
                        response_code=200,
                        response_page_path="/index.html",
                    ),
                    cloudfront.CfnDistribution.CustomErrorResponseProperty(
                        error_code=404,
                        response_code=200,
                        response_page_path="/index.html",
                    ),
                ],
            ),
        )

        # ───────────── CloudFront S3 Permission ─────────────
        from aws_cdk import aws_iam as iam
        self.website_bucket.add_to_resource_policy(
            iam.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[self.website_bucket.arn_for_objects("*")],
                principals=[iam.ServicePrincipal("cloudfront.amazonaws.com")],
                conditions={
                    "StringEquals": {
                        "AWS:SourceArn": f"arn:aws:cloudfront::{self.account}:distribution/{self.distribution.ref}"
                    }
                },
            )
        )

        # ───────────── Deploy frontend with runtime config ─────────────
        s3deploy.BucketDeployment(
            self,
            "DeployFrontend",
            sources=[
                s3deploy.Source.asset("../../frontend/dist"),
                s3deploy.Source.data(
                    "config.js",
                    "window.__GRAMMY_CONFIG__ = " + json.dumps({
                        "API_URL": api_url.rstrip("/"),
                        "USER_POOL_ID": user_pool_id,
                        "USER_POOL_CLIENT_ID": user_pool_client_id,
                    }) + ";",
                ),
            ],
            destination_bucket=self.website_bucket,
            prune=True,
            retain_on_delete=False,
            distribution=self.distribution,
            distribution_paths=["/*"],
        )

        # ───────────── Outputs ─────────────
        CfnOutput(
            self,
            "FrontendUrl",
            value=f"https://{self.distribution.attr_domain_name}",
            export_name=f"{PROJECT_NAME}-frontend-url",
        )
        CfnOutput(
            self,
            "FrontendBucketName",
            value=self.website_bucket.bucket_name,
            export_name=f"{PROJECT_NAME}-frontend-bucket",
        )
        CfnOutput(
            self,
            "CloudFrontDistributionId",
            value=self.distribution.ref,
            export_name=f"{PROJECT_NAME}-cloudfront-id",
        )
