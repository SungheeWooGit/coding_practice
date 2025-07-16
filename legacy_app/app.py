from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# Insecure in-memory store (for demo only)
TASKS = [
    {"id": 1, "title": "Fix server", "ssn": "123-45-6789", "secret": "rootpassword"},
    {"id": 2, "title": "Update docs", "credit_card": "4111-1111-1111-1111"}
]

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response

@app.route("/tasks", methods=["GET"])
def get_tasks():
    if request.method == 'OPTIONS':
        return make_response('', 204)  # Preflight response
    print("DEBUG: Returning sensitive data")  # Logs secrets (insecure)
    return jsonify(TASKS)

@app.route("/tasks", methods=["POST"])
def add_task():
    if request.method == 'OPTIONS':
        return make_response('', 204)  # Preflight response
    task = request.json
    task["id"] = len(TASKS) + 1
    TASKS.append(task)
    print("DEBUG: Added task with data: %s" % str(task))  # Logs plaintext secrets
    return jsonify(task), 201

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if request.method == 'OPTIONS':
        return make_response('', 204)  # Preflight response
    global TASKS
    TASKS = [t for t in TASKS if t["id"] != task_id]
    return jsonify({"result": "deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
