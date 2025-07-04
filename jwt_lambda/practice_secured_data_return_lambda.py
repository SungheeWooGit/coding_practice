import json
import jwt

SECRET = "secretstringonlykeptinlambda"

def lambda_handler(event, context):

    print("HEADERS RECEIVED:", json.dumps(event.get("headers", {})))

    header_str = str(event["headers"])
    auth = event["headers"].get("authorization", "")
    if not auth.startswith("Bearer "):
        return {"statusCode": 401, 
                'headers': {
                    'Content-Type': 'application/json',
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,GET,POST",
                    "Access-Control-Allow-Headers": "*"
                },
                "body": json.dumps({"error": "Failed to find token in header - " + header_str})}

    token = auth.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {"statusCode": 401, 
                'headers': {
                    'Content-Type': 'application/json',
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,GET,POST",
                    "Access-Control-Allow-Headers": "*"
                },
                "body": json.dumps({"error": "Token expired"})}
    except jwt.InvalidTokenError:
        return {"statusCode": 401, 
                'headers': {
                    'Content-Type': 'application/json',
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,GET,POST",
                    "Access-Control-Allow-Headers": "*"
                },
                "body": json.dumps({"error": "Invalid token"})}

    # Basic "encryption" for sensitive data (illustrative)
    response_data = {
        "user": payload["sub"],
        "message": "Hello from a protected Lambda!"
    }

    return {
        "statusCode": 200,
        'headers': {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,GET,POST",
            "Access-Control-Allow-Headers": "*"
        },
        "body": json.dumps(response_data)
    }