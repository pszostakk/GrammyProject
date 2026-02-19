"""Infrastructure configuration.

Routes now support specifying HTTP methods. Each route is a dict with
`path`, `handler` (the `HandlerConfig.name`) and optional `method`.
"""
import os
from typing import List, Dict
from .handlers import HandlerConfig


# Project constants
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
BACKEND = os.path.join(PROJECT_ROOT, "backend")
PROJECT_NAME = "grammy"

# CloudFront domain for CORS - update if your distribution domain changes
CLOUDFRONT_DOMAIN = "d1ha3xi7so3sx5.cloudfront.net"

# Handler configurations
HANDLERS: List[HandlerConfig] = [
    HandlerConfig(
        name="HealthHandler",
        function_name="health-get-handler",
        code_path=os.path.join(BACKEND, "health/get"),
    ),
    HandlerConfig(
        name="ProjectsGetHandler",
        function_name="projects-get-handler",
        code_path=os.path.join(BACKEND, "projects/get"),
    ),
    HandlerConfig(
        name="ProjectsGetIdHandler",
        function_name="projects-get-id-handler",
        code_path=os.path.join(BACKEND, "projects/get_id"),
    ),
    HandlerConfig(
        name="ProjectsPostHandler",
        function_name="projects-post-handler",
        code_path=os.path.join(BACKEND, "projects/post"),
    ),
    HandlerConfig(
        name="ProjectsPutHandler",
        function_name="projects-put-handler",
        code_path=os.path.join(BACKEND, "projects/put"),
    ),
    HandlerConfig(
        name="ProjectsDeleteHandler",
        function_name="projects-delete-handler",
        code_path=os.path.join(BACKEND, "projects/delete"),
    ),
    HandlerConfig(
        name="SongsGetHandler",
        function_name="songs-get-handler",
        code_path=os.path.join(BACKEND, "songs/get")
    ),
    HandlerConfig(
        name="SongsGetIdHandler",
        function_name="songs-get-id-handler",
        code_path=os.path.join(BACKEND, "songs/get_id"),
    ),
    HandlerConfig(
        name="SongsPostHandler",
        function_name="songs-post-handler",
        code_path=os.path.join(BACKEND, "songs/post")
    ),
    HandlerConfig(
        name="SongsPutHandler",
        function_name="songs-put-handler",
        code_path=os.path.join(BACKEND, "songs/put")
    ),
    HandlerConfig(
        name="SongsDeleteHandler",
        function_name="songs-delete-handler",
        code_path=os.path.join(BACKEND, "songs/delete")
    ),
    HandlerConfig(
        name="InstrumentsGetHandler",
        function_name="instruments-get-handler",
        code_path=os.path.join(BACKEND, "instruments/get"),
    ),
    HandlerConfig(
        name="InstrumentsGetIdHandler",
        function_name="instruments-get-id-handler",
        code_path=os.path.join(BACKEND, "instruments/get_id"),
    ),
    HandlerConfig(
        name="InstrumentsPostHandler",
        function_name="instruments-post-handler",
        code_path=os.path.join(BACKEND, "instruments/post"),
    ),
    HandlerConfig(
        name="InstrumentsPutHandler",
        function_name="instruments-put-handler",
        code_path=os.path.join(BACKEND, "instruments/put"),
    ),
    HandlerConfig(
        name="InstrumentsDeleteHandler",
        function_name="instruments-delete-handler",
        code_path=os.path.join(BACKEND, "instruments/delete"),
    ),
    HandlerConfig(
        name="TuningsGetHandler",
        function_name="tunings-get-handler",
        code_path=os.path.join(BACKEND, "tunings/get"),
    ),
    HandlerConfig(
        name="TuningsGetIdHandler",
        function_name="tunings-get-id-handler",
        code_path=os.path.join(BACKEND, "tunings/get_id"),
    ),
    HandlerConfig(
        name="TuningsPostHandler",
        function_name="tunings-post-handler",
        code_path=os.path.join(BACKEND, "tunings/post"),
    ),
    HandlerConfig(
        name="TuningsPutHandler",
        function_name="tunings-put-handler",
        code_path=os.path.join(BACKEND, "tunings/put"),
    ),
    HandlerConfig(
        name="TuningsDeleteHandler",
        function_name="tunings-delete-handler",
        code_path=os.path.join(BACKEND, "tunings/delete"),
    ),
]

# API routes - list of route definitions supporting different HTTP methods
# Example: {"path": "items", "handler": "ItemsHandler", "method": "POST"}
ROUTES: List[Dict[str, str]] = [
    {"path": "health", "handler": "HealthHandler", "method": "GET"},
    {"path": "projects", "handler": "ProjectsGetHandler", "method": "GET"},
    {"path": "projects/{id}", "handler": "ProjectsGetIdHandler", "method": "GET"},
    {"path": "projects", "handler": "ProjectsPostHandler", "method": "POST"},
    {"path": "projects", "handler": "ProjectsPutHandler", "method": "PUT"},
    {"path": "projects", "handler": "ProjectsDeleteHandler", "method": "DELETE"},
    {"path": "songs", "handler": "SongsGetHandler", "method": "GET"},
    {"path": "songs/{id}", "handler": "SongsGetIdHandler", "method": "GET"},
    {"path": "songs", "handler": "SongsPostHandler", "method": "POST"},
    {"path": "songs", "handler": "SongsPutHandler", "method": "PUT"},
    {"path": "songs", "handler": "SongsDeleteHandler", "method": "DELETE"},
    {"path": "instruments", "handler": "InstrumentsGetHandler", "method": "GET"},
    {"path": "instruments/{id}", "handler": "InstrumentsGetIdHandler", "method": "GET"},
    {"path": "instruments", "handler": "InstrumentsPostHandler", "method": "POST"},
    {"path": "instruments", "handler": "InstrumentsPutHandler", "method": "PUT"},
    {"path": "instruments", "handler": "InstrumentsDeleteHandler", "method": "DELETE"},
    {"path": "tunings", "handler": "TuningsGetHandler", "method": "GET"},
    {"path": "tunings/{id}", "handler": "TuningsGetIdHandler", "method": "GET"},
    {"path": "tunings", "handler": "TuningsPostHandler", "method": "POST"},
    {"path": "tunings", "handler": "TuningsPutHandler", "method": "PUT"},
    {"path": "tunings", "handler": "TuningsDeleteHandler", "method": "DELETE"},
]
