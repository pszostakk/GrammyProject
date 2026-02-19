"""Data Stack - DynamoDB, S3 backup, PITR"""
from aws_cdk import (
    Stack,
    CfnOutput,
    RemovalPolicy,
    Duration,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
)
from constructs import Construct
from .config import PROJECT_NAME


class DataStack(Stack):
    """Stack for data-related resources: DynamoDB, backups, PITR."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ───────────── DynamoDB Table with PITR ─────────────
        self.table = dynamodb.Table(
            self,
            f"{PROJECT_NAME}-table",
            table_name=f"{PROJECT_NAME}-table",
            partition_key=dynamodb.Attribute(
                name="PK",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="SK",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            point_in_time_recovery=True,  # Enable PITR
            removal_policy=RemovalPolicy.DESTROY,  # For development
        )

        # ───────────── S3 Backup Bucket ─────────────
        self.backup_bucket = s3.Bucket(
            self,
            f"{PROJECT_NAME}-backup-bucket",
            bucket_name=f"{PROJECT_NAME}-backup-{self.account}",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            versioned=True,  # Enable versioning for safety
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            lifecycle_rules=[
                s3.LifecycleRule(
                    transitions=[
                        s3.Transition(
                            transition_after=Duration.days(30),
                            storage_class=s3.StorageClass.INFREQUENT_ACCESS,
                        ),
                        s3.Transition(
                            transition_after=Duration.days(90),
                            storage_class=s3.StorageClass.GLACIER,
                        ),
                    ],
                    expiration=Duration.days(365),
                )
            ],
        )

        # ───────────── Outputs ─────────────
        CfnOutput(
            self,
            "TableName",
            value=self.table.table_name,
            export_name=f"{PROJECT_NAME}-table-name",
        )
        CfnOutput(
            self,
            "TableArn",
            value=self.table.table_arn,
            export_name=f"{PROJECT_NAME}-table-arn",
        )
        CfnOutput(
            self,
            "BackupBucketName",
            value=self.backup_bucket.bucket_name,
            export_name=f"{PROJECT_NAME}-backup-bucket",
        )
