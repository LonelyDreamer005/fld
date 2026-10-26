# Flask Student API — DevOps Practice

A simple Flask REST API with full CRUD operations, containerized with Docker,
tested with pytest, and automated with GitHub Actions CI/CD.

---

## Repository Structure

```
fld/
├── app.py                              # Flask API — the main application
├── test_app.py                         # Automated tests (pytest)
├── req.txt                             # Python dependencies
├── Dockerfile                          # Recipe to build the Docker image
├── compose.yaml                        # Run the app locally with Docker Compose
├── .gitignore                          # Files Git should not track
└── .github/
    └── workflows/
        ├── test.yml                    # CI — runs tests on every push
        └── docker-publish.yml          # CD — builds & pushes Docker image to Docker Hub
```

---

## Progress

| Week | Topic | Status |
|------|-------|--------|
| Week 1 | Backend CRUD API (GET, POST, PUT, PATCH, DELETE) | ✅ Done |
| Week 2 | Git & GitHub, source code management | ✅ Done |
| Week 3 | Docker commands, containerized app | ✅ Done |
| Week 4 | Kubernetes — integrate with Docker | ⬜ Pending |
| Week 5 | Automate with Kubernetes | ⬜ Pending |
| Week 6 | GitHub Actions — CI/CD setup | ✅ Done |
| Week 7 | Postman — manual API testing | 🟡 Partial (app ready, Postman not documented) |
| Week 8 | Automated test cases | ✅ Done |
| Week 9 | Monitoring & logging (Prometheus/Grafana) | ⬜ Pending |
| Week 10 | Terraform | ⬜ Pending |

---

## Week 1 — Backend CRUD API

**File:** `app.py`

A REST API for managing student records. Data is stored in memory (Python dictionary)
so it resets on every server restart — which is fine for practice.

### API Endpoints

| Method | Route | What it does | Response |
|--------|-------|-------------|----------|
| `GET` | `/` | Health check | `200` |
| `GET` | `/students` | Get all students | `200` + list |
| `POST` | `/students` | Add a student | `201` + new record |
| `GET` | `/students/<id>` | Get one student | `200` or `404` |
| `PUT` | `/students/<id>` | Replace a student fully | `200` or `404` |
| `PATCH` | `/students/<id>` | Update part of a student | `200` or `404` |
| `DELETE` | `/students/<id>` | Delete a student | `200` or `404` |

### Run Locally (without Docker)

```bash
# Install dependencies
pip install -r req.txt

# Start the server
python app.py
```

Expected output:
```
* Running on http://0.0.0.0:5000
```

### Try the API

```bash
# Check server is running
curl http://localhost:5000/

# Add a student
curl -X POST http://localhost:5000/students \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "course": "CS"}'

# Get all students
curl http://localhost:5000/students

# Get student with id 1
curl http://localhost:5000/students/1

# Update entire record (PUT)
curl -X PUT http://localhost:5000/students/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Bob", "course": "Math"}'

# Update only one field (PATCH)
curl -X PATCH http://localhost:5000/students/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Charlie"}'

# Delete student
curl -X DELETE http://localhost:5000/students/1
```

### PUT vs PATCH

- `PUT` — replaces the whole record. Send all fields.
- `PATCH` — updates only the fields you send. The rest stays as is.

---

## Week 2 — Git & GitHub

**Files:** `.gitignore`, commit history

The project is version-controlled on GitHub. Every change is tracked as a commit.

### Commit History

```
313ad3e  FLASK API                                 ← first version of app.py
52ed437  CI test                                   ← added tests, Docker, workflows
7f7dcab  Automate Docker image publishing           ← added CD workflow
ebcfa4c  Simplify all files for easy memorization  ← cleaned up all files
```

### Git Commands Used

```bash
git init                      # Initialize a repo (done once)
git status                    # See changed files
git add .                     # Stage all changes
git commit -m "message"       # Save a snapshot
git push origin main          # Send to GitHub
git log --oneline             # View all commits in one line each
git diff                      # See exact line changes
git remote -v                 # Check which GitHub repo you're connected to
```

### .gitignore

These are excluded from Git — they are either auto-generated, too large, or contain secrets:

```
venv/           ← local Python environment (never commit this)
__pycache__/    ← Python's bytecode cache (auto-generated)
*.pyc           ← compiled Python files (auto-generated)
.pytest_cache/  ← pytest internal cache (auto-generated)
.env            ← environment variables / passwords (never commit this)
```

---

## Week 3 — Docker

**Files:** `Dockerfile`, `compose.yaml`

Docker packages your app into an image — a portable, self-contained unit that
runs the same way on any machine.

### Dockerfile (explained line by line)

```dockerfile
FROM python:3.12-slim    # Start from official Python image
WORKDIR /app             # All commands run from /app inside the container
COPY req.txt .           # Copy requirements first (for caching)
RUN pip install -r req.txt  # Install packages into the image
COPY app.py .            # Copy your app code
EXPOSE 5000              # Document that the app uses port 5000
CMD ["python", "app.py"] # Command that runs when container starts
```

> `req.txt` is copied before `app.py` so Docker can cache the `pip install` layer.
> If only your code changes, Docker reuses the cached packages — faster rebuilds.

### compose.yaml (explained)

```yaml
services:
  app:
    build: .          # Build image from Dockerfile in this directory
    ports:
      - "5000:5000"   # Your machine port 5000 → container port 5000
```

### Docker Commands

```bash
# Build image manually
docker build -t flask-student-api .

# Run container manually
docker run -p 5000:5000 flask-student-api

# Run with Compose (recommended)
docker compose up

# Run in background (detached mode)
docker compose up -d

# Stop and remove containers
docker compose down

# View running containers
docker ps

# View all containers (including stopped)
docker ps -a

# View container logs
docker logs <container_id>

# View all images
docker images

# Remove an image
docker rmi flask-student-api
```

---

## Week 4 & 5 — Kubernetes

> **Status: Not implemented yet.**

Kubernetes (K8s) manages multiple containers across many machines at scale.
For this project, the plan is to create manifest files in a `k8s/` folder.

**What needs to be done:**
1. Install [minikube](https://minikube.sigs.k8s.io/) for local Kubernetes
2. Create `k8s/deployment.yaml` — tells K8s to run 2 copies of the container
3. Create `k8s/service.yaml` — exposes the app on a port
4. Run `kubectl apply -f k8s/`

---

## Week 6 — GitHub Actions (CI/CD)

**Files:** `.github/workflows/test.yml`, `.github/workflows/docker-publish.yml`

GitHub Actions runs automation tasks in the cloud every time you push code.

### How it works

```
git push origin main
       │
       ├── test.yml (CI) ─── runs on every push and pull request
       │       ↓
       │   1. Checkout code
       │   2. Install Python 3.12
       │   3. pip install -r req.txt
       │   4. pytest
       │   → Green ✅ or Red ❌ check shown on GitHub
       │
       └── docker-publish.yml (CD) ─── runs only on push to main
               ↓
           1. Checkout code
           2. Set up Docker Buildx
           3. Login to Docker Hub (using GitHub Secrets)
           4. Build image from Dockerfile
           5. Push image to Docker Hub
```

### CI Workflow — `test.yml`

```yaml
name: Test
on: [push, pull_request]   # Trigger on every push and PR
jobs:
  test:
    runs-on: ubuntu-latest  # GitHub spins up a fresh Ubuntu VM
    steps:
      - uses: actions/checkout@v4         # Download your code
      - uses: actions/setup-python@v5     # Install Python
        with:
          python-version: "3.12"
      - run: pip install -r req.txt       # Install dependencies
      - run: pytest                       # Run all tests
```

### CD Workflow — `docker-publish.yml`

```yaml
name: Docker
on:
  push:
    branches: [main]   # Only runs when you push to main
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3        # Login to Docker Hub
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      - uses: docker/build-push-action@v6   # Build + push
        with:
          push: true
          tags: ${{ secrets.DOCKERHUB_USERNAME }}/flask-student-api:latest
```

### GitHub Secrets

`DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` are not written in the file.
They are stored in GitHub: **Repo → Settings → Secrets and variables → Actions**.
This keeps credentials out of the code.

---

## Week 7 — Postman (Manual API Testing)

> **Status: The API is ready. Postman testing is not yet documented.**

Postman is a GUI tool for sending HTTP requests to test APIs manually.

**What to do:**
1. Download Postman from [postman.com](https://postman.com)
2. Start the app: `python app.py`
3. Create a new Collection called `Student API`
4. Add and test these requests:

| Name | Method | URL | Body (JSON) |
|------|--------|-----|-------------|
| Home | GET | `http://localhost:5000/` | — |
| Get all students | GET | `http://localhost:5000/students` | — |
| Add student | POST | `http://localhost:5000/students` | `{"name":"Alice","course":"CS"}` |
| Get student by ID | GET | `http://localhost:5000/students/1` | — |
| Full update | PUT | `http://localhost:5000/students/1` | `{"name":"Bob","course":"Math"}` |
| Partial update | PATCH | `http://localhost:5000/students/1` | `{"name":"Charlie"}` |
| Delete student | DELETE | `http://localhost:5000/students/1` | — |

---

## Week 8 — Automated Test Cases

**File:** `test_app.py`

Tests are written with `pytest` and use Flask's built-in test client.
No real HTTP server is started — Flask simulates requests internally.

```python
from app import app

client = app.test_client()   # Simulate a browser/API client

def test_home():
    res = client.get("/")
    assert res.status_code == 200        # 200 = OK

def test_get_students():
    res = client.get("/students")
    assert res.status_code == 200

def test_add_student():
    res = client.post("/students", json={"name": "Alice", "course": "CS"})
    assert res.status_code == 201        # 201 = Created
```

### Run tests

```bash
pytest           # Run all tests
pytest -v        # Verbose — shows each test name
```

Expected output:
```
test_app.py::test_home           PASSED
test_app.py::test_get_students   PASSED
test_app.py::test_add_student    PASSED
3 passed in 0.25s
```

---

## Week 9 — Monitoring & Logging

> **Status: Not implemented yet.**

The plan is to add Prometheus (metrics collection) and Grafana (dashboard).

**What needs to be done:**
1. Add `prometheus-flask-exporter` to `req.txt`
2. Add 2 lines to `app.py` to expose metrics at `/metrics`
3. Add Prometheus and Grafana services to `compose.yaml`

---

## Week 10 — Terraform

> **Status: Not implemented yet.**

Terraform is Infrastructure as Code — write `.tf` files to provision cloud resources
instead of clicking in AWS/GCP/Azure consoles.

---

## Dependencies

**`req.txt`**

```
flask     ← web framework the API is built on
pytest    ← testing framework to run test_app.py
```

Install:
```bash
pip install -r req.txt
```

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/LonelyDreamer005/fld.git
cd fld

# 2. Install dependencies
pip install -r req.txt

# 3. Run the app
python app.py

# 4. Run tests
pytest

# 5. Run with Docker
docker compose up
```

---

## How Everything Connects

```
req.txt
  ├── read by → Dockerfile (pip install during image build)
  └── read by → test.yml (pip install before running pytest)

app.py
  ├── tested by → test_app.py
  ├── packaged by → Dockerfile
  └── run inside container started by → compose.yaml

Dockerfile
  ├── used by → compose.yaml (build: .)
  └── used by → docker-publish.yml (build and push to Docker Hub)

test_app.py
  ├── imports → app.py
  └── run by → test.yml (via pytest)

test.yml (CI)
  └── runs on every push → installs deps → runs pytest → shows pass/fail on GitHub

docker-publish.yml (CD)
  └── runs on push to main → builds Docker image → pushes to Docker Hub
```
