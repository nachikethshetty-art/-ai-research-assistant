╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║          🐳 DOCKER & DEPLOYMENT GUIDELINES                                ║
║                                                                            ║
║     Complete instructions for containerization & deployment               ║
║     Your project is hackathon-ready with Docker!                          ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝


═════════════════════════════════════════════════════════════════════════════
WHAT YOU HAVE NOW
═════════════════════════════════════════════════════════════════════════════

FILES CREATED:
  ✅ server/Dockerfile - Production Docker image configuration
  ✅ docker-compose.yml - Full stack (Ollama + Research Assistant)
  ✅ .dockerignore - Exclude unnecessary files from image

WHAT THEY DO:
  • Dockerfile: Packages your entire app into a single runnable image
  • docker-compose.yml: Orchestrates Ollama + app together (for local dev)
  • .dockerignore: Keeps Docker image lean (faster builds)


═════════════════════════════════════════════════════════════════════════════
QUICK START: BUILD & RUN LOCALLY (5 MINUTES)
═════════════════════════════════════════════════════════════════════════════

OPTION 1: Using docker-compose (Simplest - Recommended)
──────────────────────────────────────────────────────

Terminal 1: Start the full stack
─────────────────────────────────
$ cd /Users/amshumathshetty/Desktop/ai-research-assistant
$ docker-compose up

Expected Output:
  Creating research-ollama ... done
  Creating research-assistant ... done
  [ollama] Loading, please wait...
  [research-assistant] streamlit run app/streamlit_app.py
  [research-assistant] URL: http://localhost:8501

⏱️ Time: 30-60 seconds (first time)

Then:
  Open browser: http://localhost:8501
  ✅ Dashboard appears
  ✅ Ollama connected (shows ✅ in sidebar)
  ✅ All 5 tabs visible
  ✅ Ready to demo!

Stop:
  Press Ctrl+C in terminal
  $ docker-compose down


OPTION 2: Using individual docker commands
───────────────────────────────────────────

Terminal 1: Start Ollama
────────────────────────
$ docker run -d \
  --name research-ollama \
  -p 11434:11434 \
  ollama/ollama

Wait 10 seconds, then pull Mistral:
$ docker exec research-ollama ollama pull mistral

Expected:
  Pulling manifest
  Pulling [...]
  Success

Terminal 2: Build and run your app
──────────────────────────────────
$ cd /Users/amshumathshetty/Desktop/ai-research-assistant
$ docker build -t research-assistant:v2.0 -f server/Dockerfile .

Expected:
  Step 1/12 : FROM python:3.11-slim
  Step 2/12 : WORKDIR /app
  ...
  Successfully built [hash]
  Successfully tagged research-assistant:v2.0

⏱️ Time: 2-3 minutes (first time only)

Run the app:
$ docker run -p 8501:8501 \
  -e OLLAMA_HOST=http://docker.for.mac.localhost:11434 \
  research-assistant:v2.0

Expected:
  2024-03-23 10:00:00 streamlit run...
  URL: http://0.0.0.0:8501

Then:
  Open browser: http://localhost:8501
  ✅ Ready to demo!


═════════════════════════════════════════════════════════════════════════════
UNDERSTANDING THE DOCKERFILE
═════════════════════════════════════════════════════════════════════════════

What each line does:

FROM python:3.11-slim
  → Starts with lightweight Python 3.11 image
  → slim = removes unnecessary packages

WORKDIR /app
  → Creates /app directory inside container
  → All commands run from here

RUN apt-get update && apt-get install -y ...
  → Installs system dependencies (curl, git, build tools)
  → Ensures compatibility with all packages

COPY requirements.txt .
  → Copies your requirements.txt from local to container

RUN pip install --no-cache-dir -r requirements.txt
  → Installs all Python packages
  → --no-cache-dir = smaller image size

COPY . .
  → Copies entire project into container
  → All your source code

RUN mkdir -p /app/data
  → Creates data directory for feedback.json

EXPOSE 8501
  → Declares port 8501 (Streamlit default)
  → Important for documentation

HEALTHCHECK
  → Tells Docker when the container is "healthy"
  → Ensures app is responsive

ENV PYTHONUNBUFFERED=1
  → Python output appears immediately (no buffering)

CMD ["streamlit", "run", ...]
  → Default command when container starts
  → Runs your Streamlit app


═════════════════════════════════════════════════════════════════════════════
UNDERSTANDING docker-compose.yml
═════════════════════════════════════════════════════════════════════════════

Two Services:

SERVICE 1: ollama
────────────────
image: ollama/ollama:latest
  → Official Ollama image
  → Contains LLM runtime

ports:
  - "11434:11434"
  → Host:Container port mapping
  → Access at localhost:11434

volumes:
  - ollama_data:/root/.ollama
  → Persist models across restarts
  → Named volume (Docker-managed)

healthcheck:
  → Verifies Ollama is responding
  → Waits before starting app


SERVICE 2: research-assistant
────────────────────────────
build:
  → Build from Dockerfile
  → Context = current directory

depends_on:
  → Waits for ollama to be healthy
  → Ensures proper startup order

volumes:
  → Mount local files into container
  → Hot-reload for development
  → /app/data = persistent storage

environment:
  → Pass variables to app
  → OLLAMA_HOST = connection string
  → Streamlit settings


═════════════════════════════════════════════════════════════════════════════
DEPLOYMENT SCENARIOS
═════════════════════════════════════════════════════════════════════════════

SCENARIO 1: LOCAL TESTING (For Hackathon Prep)
──────────────────────────────────────────────

Goal: Test before submission
Time: 5 minutes
Steps:
  1. $ docker-compose up
  2. Open http://localhost:8501
  3. Test all features
  4. $ docker-compose down

Result: ✅ Confident your code works
Judges see: Your code works locally in Docker


SCENARIO 2: HACKATHON SUBMISSION (Just Include Dockerfile)
─────────────────────────────────────────────────────────

Goal: Submit to hackathon with Docker
Time: 0 (files already created!)
Steps:
  1. Commit files: git add server/Dockerfile docker-compose.yml .dockerignore
  2. git commit -m "Add Docker containerization"
  3. git push origin main

Result: ✅ Judges can run: docker build & docker run
Judges see: "Professional setup, can deploy anywhere"


SCENARIO 3: HF SPACES DEPLOYMENT (Persistent Demo)
──────────────────────────────────────────────────

Goal: Live demo for judges (accessible anytime)
Time: 30 minutes
Benefits:
  ✓ Judges can test anytime
  ✓ No setup required from their side
  ✓ Impresses them with deployment skills
  ✓ Works after hackathon

Steps:
  1. Create HF account (if needed)
  2. Create new Space (choose Docker SDK)
  3. git remote add hf https://huggingface.co/spaces/[username]/research-assistant
  4. Copy server/Dockerfile to root
  5. git push hf main
  6. Wait 5-10 minutes for build
  7. Live at: https://[username]-research-assistant.hf.space

Result: ✅ App running in cloud
Judges see: "This person knows cloud deployment!"

Detailed HF Spaces instructions in HF_SPACES_DEPLOYMENT.md (coming next)


SCENARIO 4: PRODUCTION DEPLOYMENT (After Winning)
────────────────────────────────────────────────

Goal: Run for real users (scaling, reliability)
Time: 1-2 hours
Options:
  a) AWS ECS (Elastic Container Service)
  b) Azure Container Instances
  c) Google Cloud Run
  d) DigitalOcean App Platform
  e) Heroku (with Docker support)

Process:
  1. Push Docker image to container registry (ECR, ACR, etc.)
  2. Configure auto-scaling
  3. Setup load balancer
  4. Configure domain & SSL
  5. Deploy

Kubernetes NOT needed yet:
  ✗ Overengineering for current scale
  ✓ Docker + simple orchestration is enough
  → Add K8s only when you have 1000+ concurrent users


═════════════════════════════════════════════════════════════════════════════
TROUBLESHOOTING DOCKER ISSUES
═════════════════════════════════════════════════════════════════════════════

ISSUE: "Cannot connect to Docker daemon"
───────────────────────────────────────
Fix: Start Docker Desktop
  macOS: $ open /Applications/Docker.app
  
Verify:
  $ docker --version
  Docker version 24.0.0+ (should show version)


ISSUE: "Port 8501 already in use"
───────────────────────────────────
Fix Option 1: Stop existing container
  $ docker ps
  $ docker stop [container_id]

Fix Option 2: Use different port
  $ docker run -p 8502:8501 research-assistant:v2.0
  Then open http://localhost:8502


ISSUE: "Ollama connection refused"
──────────────────────────────────
Fix: Ensure Ollama is running
  Terminal 1: $ docker run -p 11434:11434 ollama/ollama
  Terminal 2: $ docker exec [ollama_id] ollama pull mistral
  Terminal 3: $ docker run -e OLLAMA_HOST=http://docker.for.mac.localhost:11434 research-assistant:v2.0


ISSUE: "Requirements installation fails"
─────────────────────────────────────────
Fix: Rebuild without cache
  $ docker build --no-cache -t research-assistant:v2.0 .

Or check Python version compatibility:
  $ python3 --version  # Should be 3.11+


ISSUE: "Health check failing"
──────────────────────────────
Wait 40 seconds (health check grace period)
Check logs:
  $ docker logs [container_id]

If still failing, verify Streamlit is accessible:
  $ curl http://localhost:8501/_stcore/health


ISSUE: "Volume mount permissions denied"
─────────────────────────────────────────
Fix: Check file permissions
  $ ls -la data/
  $ chmod -R 755 data/

Or rebuild with proper permissions:
  $ docker-compose down
  $ docker-compose up --build


═════════════════════════════════════════════════════════════════════════════
DOCKER COMMANDS REFERENCE
═════════════════════════════════════════════════════════════════════════════

BUILD:
  $ docker build -t research-assistant:v2.0 -f server/Dockerfile .
  → Build image from Dockerfile

RUN:
  $ docker run -p 8501:8501 research-assistant:v2.0
  → Create and start container from image

LIST:
  $ docker ps
  → List running containers

  $ docker ps -a
  → List all containers (running + stopped)

  $ docker images
  → List all images

LOGS:
  $ docker logs [container_id]
  → View container output

  $ docker logs -f [container_id]
  → Follow logs (live streaming)

EXECUTE:
  $ docker exec -it [container_id] bash
  → Run bash shell inside container

STOP/START:
  $ docker stop [container_id]
  → Stop running container

  $ docker start [container_id]
  → Start stopped container

REMOVE:
  $ docker rm [container_id]
  → Delete container

  $ docker rmi research-assistant:v2.0
  → Delete image

DOCKER-COMPOSE:
  $ docker-compose up
  → Start all services

  $ docker-compose down
  → Stop all services

  $ docker-compose logs
  → View logs from all services

  $ docker-compose build
  → Rebuild images


═════════════════════════════════════════════════════════════════════════════
BEST PRACTICES FOR HACKATHON SUBMISSION
═════════════════════════════════════════════════════════════════════════════

✅ DO:
  ✓ Include Dockerfile (shows maturity)
  ✓ Include docker-compose.yml (shows orchestration knowledge)
  ✓ Test locally with Docker before submitting
  ✓ Document setup in README
  ✓ Keep image size reasonable (< 2GB)
  ✓ Use health checks (shows production thinking)
  ✓ Version your image (v2.0)
  ✓ Test port accessibility

❌ DON'T:
  ✗ Commit .dockerignore without actually using Docker
  ✗ Use outdated base images
  ✗ Hardcode secrets in Dockerfile
  ✗ Run as root (security risk)
  ✗ Make images unnecessarily large
  ✗ Forget to test before submitting


═════════════════════════════════════════════════════════════════════════════
UPDATE YOUR README.md
═════════════════════════════════════════════════════════════════════════════

Add this section to your README.md:

---

## 🐳 Docker Deployment

### Quick Start with Docker

**Requires**: Docker Desktop installed

```bash
# Clone and navigate
cd ai-research-assistant

# Option 1: Full stack (Ollama + App)
docker-compose up

# Option 2: Just the app (if Ollama already running)
docker build -t research-assistant:v2.0 -f server/Dockerfile .
docker run -p 8501:8501 research-assistant:v2.0

# Open browser
open http://localhost:8501
```

### What's in the Docker Image?
- ✅ Python 3.11
- ✅ All dependencies from requirements.txt
- ✅ Your complete application
- ✅ Health checks for reliability
- ✅ Optimized for production

### Troubleshooting Docker
See [Docker Troubleshooting](DOCKER_DEPLOYMENT_GUIDELINES.md#troubleshooting-docker-issues)

---


═════════════════════════════════════════════════════════════════════════════
NEXT STEP: HF SPACES DEPLOYMENT
═════════════════════════════════════════════════════════════════════════════

After you test locally with Docker, if you want a persistent cloud demo:

FILE: HF_SPACES_DEPLOYMENT.md (to be created)

Contains:
  ✅ HF Spaces account setup
  ✅ Space creation (Docker SDK)
  ✅ Git configuration
  ✅ Deployment steps
  ✅ Custom domain setup (optional)
  ✅ Monitoring & scaling
  ✅ Cost management


═════════════════════════════════════════════════════════════════════════════
FINAL CHECKLIST
═════════════════════════════════════════════════════════════════════════════

BEFORE HACKATHON SUBMISSION:
  ☐ Docker installed and running
  ☐ Build image: docker build -t research-assistant:v2.0 .
  ☐ Run container: docker run -p 8501:8501 research-assistant:v2.0
  ☐ Open http://localhost:8501
  ☐ Test all 5 tabs work
  ☐ Test queries work
  ☐ Test abstracts generation
  ☐ Test plagiarism detection
  ☐ Commit Dockerfile, docker-compose.yml, .dockerignore
  ☐ Push to git repository

JUDGES WILL:
  ☐ Review Dockerfile (shows maturity)
  ☐ Run docker build (verifies reproducibility)
  ☐ Run docker run (tests your app)
  ☐ Access http://localhost:8501 (sees your dashboard)
  ☐ Test features (asks questions, generates content)
  ☐ Rate your containerization (DevOps skills)


═════════════════════════════════════════════════════════════════════════════
SUMMARY: YOU'RE READY!
═════════════════════════════════════════════════════════════════════════════

✅ Code is compliant with hackathon guidelines
✅ Core concept is maintained (7 phases + v2.0)
✅ Dockerfile is production-ready
✅ docker-compose.yml handles dependencies
✅ .dockerignore keeps image lean

Now:
  1. Test: docker-compose up
  2. Verify: http://localhost:8501 works
  3. Submit: Include Dockerfile in repo
  4. Win! 🏆

═════════════════════════════════════════════════════════════════════════════
