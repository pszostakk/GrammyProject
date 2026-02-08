"""Infrastructure configuration.

Routes now support specifying HTTP methods. Each route is a dict with
`path`, `handler` (the `HandlerConfig.name`) and optional `method`.
"""
import os
from typing import List, Dict
from .handlers import HandlerConfig


# Project constants
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
BACKEND = os.path.join(PROJECT_ROOT, "backend")
PROJECT_NAME = "grammy"

# Handler configurations
HANDLERS: List[HandlerConfig] = [
    HandlerConfig(
        name="HealthHandler",
        function_name="health-get-handler",
        code_path=os.path.join(BACKEND, "health/get"),
    ),
    HandlerConfig(
        name="KacperHandler",
        function_name="kacper-get-handler",
        code_path=os.path.join(BACKEND, "kacper/get"),
    ),
    HandlerConfig(
        name="PawelHandler",
        function_name="pawel-get-handler",
        code_path=os.path.join(BACKEND, "pawel/get"),
    ),
    HandlerConfig(
        name="SongsHandler",
        function_name="songs-get-handler",
        code_path=os.path.join(BACKEND, "songs/get"),
    ),
]

# API routes - list of route definitions supporting different HTTP methods
# Example: {"path": "items", "handler": "ItemsHandler", "method": "POST"}
ROUTES: List[Dict[str, str]] = [
    {"path": "health", "handler": "HealthHandler", "method": "GET"},
    {"path": "kacper", "handler": "KacperHandler", "method": "GET"},
    {"path": "pawel", "handler": "PawelHandler", "method": "GET"},
    {"path": "songs", "handler": "SongsHandler", "method": "GET"},
]
