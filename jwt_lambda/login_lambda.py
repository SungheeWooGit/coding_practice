import json
import jwt
import datetime

SECRET = "secretstringonlykeptinlambda"  # Store in AWS Secrets Manager in prod
EXPIRATION_SECONDS = 3600  # 1 hour

def lambda_handler(event, context):
    body = json.loads(event["body"])

    if body.get("username") != "admin" or body.get("password") != "password":
        return {"statusCode": 401, "body": json.dumps({"error": "Invalid credentials"})}

    payload = {
        "sub": "admin",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=EXPIRATION_SECONDS),
    }
    token = jwt.encode(payload, SECRET, algorithm="HS256")

    return {
        "statusCode": 200,
        'headers': {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,GET,POST",
            "Access-Control-Allow-Headers": "*"
        },
        "body": json.dumps({"token": token})
    }