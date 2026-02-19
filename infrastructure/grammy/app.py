#!/usr/bin/env python3
import os

import aws_cdk as cdk

from grammy.data_stack import DataStack
from grammy.backend_stack import BackendStack
from grammy.frontend_stack import FrontendStack


app = cdk.App()

# Deploy stacks in order with cross-stack dependencies
data_stack = DataStack(app, "GrammyDataStack")

backend_stack = BackendStack(
    app,
    "GrammyBackendStack",
    table_name=data_stack.table.table_name,
    table_arn=data_stack.table.table_arn,
)

frontend_stack = FrontendStack(
    app,
    "GrammyFrontendStack",
    api_url=backend_stack.base_api.url,
    user_pool_id=backend_stack.user_pool.user_pool_id,
    user_pool_client_id=backend_stack.user_pool_client.user_pool_client_id,
)

# Add explicit dependencies
backend_stack.add_dependency(data_stack)
frontend_stack.add_dependency(backend_stack)

app.synth()
