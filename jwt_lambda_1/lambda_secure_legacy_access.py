import json
import jwt
import requests
import os
import datetime

JWT_SECRET = "keyfordemo"
JWT_ALGORITHM = "HS256"

LEGACY_API_URL = "http://13.52.150.213:9000/tasks"

def lambda_handler(event, context):
    # Preflight CORS
    method = event.get('httpMethod', 'GET')
    if method == 'OPTIONS':
        # Preflight CORS response
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization"
            },
            "body": json.dumps({"message": "CORS preflight OK"})
        }
    
    try:
        body = json.loads(event.get("body", "{}"))
        username = body.get("username")

        # Generate JWT
        payload = {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=120)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

        # # Get JWT from Authorization header
        # auth_header = event['headers'].get('Authorization', '')
        # if not auth_header.startswith('Bearer '):
        #     return _response(401, {"message": "Missing or invalid Authorization header"})
        # token = auth_header.split(' ')[1]

        # Validate JWT
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        # Forward the request to legacy API
        legacy_response = requests.get(LEGACY_API_URL)
        tasks = legacy_response.json()

        # Scrub sensitive data (example: remove PII fields)
        for task in tasks:
            task.pop('ssn', None)
            task.pop('password', None)

        return _response(200, tasks)

    except jwt.ExpiredSignatureError:
        return _response(401, {"message": "Token expired"})
    except jwt.InvalidTokenError:
        return _response(401, {"message": "Invalid token"})
    except Exception as e:
        return _response(500, {"error": str(e)})

def _response(status, body):
    return {
        "statusCode": status,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        "body": json.dumps(body)
    }
