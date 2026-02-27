import os
import json
import boto3
import ulid
from datetime import datetime
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))

        project_name = body.get("projectName")
        is_public = body.get("isPublic", False)
        contributors = body.get("contributors", [])

        if not project_name:
            return _response(400, {"message": "projectName is required"})

        # Authenticated user from Cognito
        owner_sub = event["requestContext"]["authorizer"]["claims"]["sub"]

        project_id = str(ulid.new())
        now = datetime.utcnow().isoformat()

        # 1️⃣ Create PROJECT META item
        project_item = {
            "PK": f"PROJECT#{project_id}",
            "SK": "META",
            "entityType": "PROJECT",
            "projectId": project_id,
            "projectName": project_name,
            "ownerId": f"USER#{owner_sub}",
            "isPublic": str(is_public).lower(),
            "createdAt": now,
            "modifiedAt": now,
        }

        table.put_item(Item=project_item)

        # 2️⃣ Add owner automatically as contributor with write access
        owner_contributor_item = {
            "PK": f"PROJECT#{project_id}",
            "SK": f"CONTRIBUTOR#USER#{owner_sub}",
            "entityType": "PROJECT_CONTRIBUTOR",
            "writePermissions": True,
            "addedAt": now,
        }

        table.put_item(Item=owner_contributor_item)

        # 3️⃣ Add additional contributors
        for contributor in contributors:
            user_id = contributor.get("userId")
            write_permissions = contributor.get("writePermissions", False)

            if not user_id:
                continue

            contributor_item = {
                "PK": f"PROJECT#{project_id}",
                "SK": f"CONTRIBUTOR#USER#{user_id}",
                "entityType": "PROJECT_CONTRIBUTOR",
                "writePermissions": write_permissions,
                "addedAt": now,
            }

            table.put_item(Item=contributor_item)

        return _response(
            201, {"projectId": project_id, "message": "Project created successfully"}
        )

    except ClientError as e:
        return _response(500, {"message": "Database error", "error": str(e)})

    except Exception as e:
        return _response(500, {"message": "Internal server error", "error": str(e)})


def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }
