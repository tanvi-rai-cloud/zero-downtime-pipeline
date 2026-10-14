"""A small web API used to practise Docker, Terraform, Ansible, Kubernetes and CI/CD."""
import os
import socket

from flask import Flask, jsonify, request

app = Flask(__name__)

# The version comes from an environment variable so we can show
# a v1 -> v2 rolling upgrade later without changing code.
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

# In-memory store: fine for a demo, data resets when the app restarts.
NOTES = []


@app.get("/health")
def health():
    """Used by Docker, Kubernetes and monitoring to check the app is alive."""
    return jsonify(status="ok"), 200


@app.get("/version")
def version():
    """Shows which version and which container answered the request."""
    return jsonify(version=APP_VERSION, host=socket.gethostname()), 200


@app.get("/notes")
def list_notes():
    return jsonify(notes=NOTES), 200


@app.post("/notes")
def add_note():
    data = request.get_json(silent=True) or {}
    text = str(data.get("text", "")).strip()
    if not text:
        return jsonify(error="'text' is required"), 400
    note = {"id": len(NOTES) + 1, "text": text}
    NOTES.append(note)
    return jsonify(note), 201


if __name__ == "__main__":
    # Local development only; in Docker we use gunicorn instead.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
