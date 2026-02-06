"""Lambda handler definitions and factory."""
from typing import NamedTuple
from aws_cdk import aws_lambda as _lambda, Duration


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
    return _lambda.Function(
        stack,
        config.name,
        function_name=f"{project_name}-{config.function_name}",
        runtime=config.runtime,
        handler=config.handler,
        code=_lambda.Code.from_asset(config.code_path),
        timeout=Duration.seconds(config.timeout_seconds),
        memory_size=config.memory_size,
    )
