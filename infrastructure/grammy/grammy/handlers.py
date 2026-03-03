"""Lambda handler definitions and factory."""
from typing import NamedTuple
from aws_cdk import aws_lambda as _lambda, Duration, BundlingOptions


class HandlerConfig(NamedTuple):
    """Configuration for a Lambda handler."""
    name: str
    function_name: str
    code_path: str
    runtime: _lambda.Runtime = _lambda.Runtime.PYTHON_3_14
    handler: str = "index.handler"
    timeout_seconds: int = 10
    memory_size: int = 256


def create_lambda_function(
    stack,
    config: HandlerConfig,
    project_name: str
) -> _lambda.Function:
    """Create a Lambda function from configuration.
    
    Args:
        stack: CDK Stack instance
        config: HandlerConfig with function details
        project_name: Project name for naming
        
    Returns:
        Configured Lambda Function
    """
    # Use bundling to include dependencies from handler's requirements.txt
    bundling_options = BundlingOptions(
        image=_lambda.Runtime.PYTHON_3_14.bundling_image,
        command=[
            "bash", "-c", 
            "if [ -f requirements.txt ]; then pip install -r requirements.txt -t /asset-output; fi && cp -r /asset-input/* /asset-output/"
        ]
    )
    
    return _lambda.Function(
        stack,
        config.name,
        function_name=f"{project_name}-{config.function_name}",
        runtime=config.runtime,
        handler=config.handler,
        code=_lambda.Code.from_asset(
            config.code_path,
            bundling=bundling_options
        ),
        timeout=Duration.seconds(config.timeout_seconds),
        memory_size=config.memory_size
    )
