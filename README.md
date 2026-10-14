# Zero-Downtime Deployment Pipeline on AWS

A personal project to practise the full DevOps workflow: a small Python API that is
containerised, provisioned with Terraform, configured with Ansible, deployed to
Kubernetes (k3s) through a GitHub Actions pipeline, monitored with Prometheus and
Grafana, and upgraded from v1 to v2 with zero downtime.

## Status

- [x] Week 1: Python API, tests, Docker image
- [ ] Weeks 2–3: AWS infrastructure with Terraform
- [ ] Week 3: Server configuration with Ansible
- [ ] Week 4: Kubernetes (k3s) deployment
- [ ] Week 5: CI/CD with GitHub Actions
- [ ] Week 6: Monitoring with Prometheus and Grafana
- [ ] Week 7: Zero-downtime rolling upgrade and rollback demo

## The app

| Endpoint      | Method | Purpose                                         |
|---------------|--------|-------------------------------------------------|
| `/health`     | GET    | Liveness check for Docker, Kubernetes, monitoring |
| `/version`    | GET    | Returns app version and which container answered |
| `/notes`      | GET    | Lists notes                                     |
| `/notes`      | POST   | Adds a note: `{"text": "..."}`                  |

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
python -m pytest -v              # run the tests
python app.py                    # app runs on http://localhost:8080
```

## Run with Docker

```bash
docker build -t notes-api:1.0.0 .
docker run -d -p 8080:8080 --name notes-api notes-api:1.0.0
curl http://localhost:8080/health
curl http://localhost:8080/version
curl -X POST http://localhost:8080/notes -H "Content-Type: application/json" -d '{"text":"hello"}'
docker ps                        # STATUS should show (healthy) after ~30s
```

To simulate a new release:

```bash
docker run -d -p 8081:8080 -e APP_VERSION=2.0.0 --name notes-api-v2 notes-api:1.0.0
curl http://localhost:8081/version
```

## Design choices

- **Version from an environment variable**: lets the same image show v1 and v2 for the
  rolling-upgrade demo.
- **gunicorn instead of Flask's dev server**: the dev server isn't meant for production.
- **Non-root container user**: limits damage if the app is compromised.
- **Docker HEALTHCHECK on `/health`**: the same endpoint later becomes the Kubernetes
  readiness/liveness probe and the monitoring target.
