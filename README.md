# Automated CI/CD Deployment Pipeline for Containerized Applications

[![deploy](https://github.com/Jhonnikek/aurora/actions/workflows/deploy.yml/badge.svg)](https://github.com/Jhonnikek/aurora/actions/workflows/deploy.yml)
![Docker](https://img.shields.io/badge/Docker-containerized-2496ED?logo=docker&logoColor=white)
![OCI](https://img.shields.io/badge/Oracle_Cloud-Infrastructure-F80000?logo=oracle&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?logo=githubactions&logoColor=white)

> A fully automated DevOps workflow that builds, packages, and deploys a Python Discord bot to a cloud server on every `git push` — with zero manual intervention.

---

## Why this project

Manual deployments are slow and error-prone. This pipeline eliminates them entirely: a single `git push` to `main` triggers an automated sequence that builds a fresh Docker image, pushes it to a registry, and restarts the live service on a remote cloud instance — all in under 2 minutes, with no SSH session required from the developer.

---

## Architecture

```
Developer                GitHub                        Oracle Cloud (OCI)
─────────                ──────                        ──────────────────
git push main  ──────►  Actions runner starts
                         │
                         ├─ Checkout code
                         ├─ Login to GHCR
                         ├─ Build multi-stage image
                         ├─ Push image to GHCR  ──────► ghcr.io/Jhonniek/...
                         │
                         ├─ SCP compose.yaml ──────────► Ubuntu VM
                         └─ SSH: docker compose up ────► Running container ✓
```

**Full cycle time: ~90 seconds from push to live.**

---

## Core technologies

| Layer | Technology | Role |
|---|---|---|
| Cloud infrastructure | Oracle Cloud Infrastructure (OCI) | Ubuntu compute instance hosting the service |
| CI/CD orchestration | GitHub Actions | Automates the full build-deploy sequence |
| Containerization | Docker + Docker Compose | Packages and runs the application |
| Image registry | GitHub Container Registry (GHCR) | Stores versioned Docker images |
| Remote access | SSH + SCP (appleboy actions) | Secure file transfer and command execution |
| Runtime | Python + `uv` | Application logic and dependency management |

---

## How it works

Every push to `main` triggers `.github/workflows/deploy.yml`, which runs five sequential steps:

**1. Checkout** — the runner fetches the latest code.

**2. Authenticate** — the workflow logs into GHCR using `GITHUB_TOKEN` (no hardcoded credentials).

**3. Build & push** — a multi-stage Dockerfile produces a lean production image and pushes it to the registry.

**4. Transfer config** — `appleboy/scp-action` uploads the latest `compose.yaml` to the OCI instance over SSH.

**5. Rolling restart** — `appleboy/ssh-action` runs `docker compose pull && docker compose up -d` on the server, replacing the running container with zero downtime.

Application secrets (Discord token, etc.) live in an `.env` file on the server, never in the repository or workflow logs.

---

## Repository structure

```
├── .github/
│   └── workflows/
│       └── deploy.yml       # CI/CD pipeline definition
├── cogs/                    # Discord bot feature modules
├── bot.py                   # Application entry point
├── pyproject.toml           # Dependency manifest (uv)
├── uv.lock                  # Locked dependency versions
├── Dockerfile               # Multi-stage container build
├── compose.yaml             # Production orchestration config
├── compose.dev.yaml         # Local development config
└── README.md
```

---

## Setup & replication

### Prerequisites

- An OCI compute instance (Ubuntu) with Docker and Docker Compose installed
- SSH access to the instance
- A GitHub repository with Actions enabled

### Required secrets

Configure these in **Settings → Secrets and variables → Actions**:

| Secret | Description |
|---|---|
| `ORACLE_IP` | Public IP of the OCI instance |
| `ORACLE_USER` | SSH username (e.g. `ubuntu`) |
| `ORACLE_SSH_KEY` | Private key for SSH access |
| `GITHUB_TOKEN` | Auto-provided by GitHub Actions for GHCR auth |

### Local development

```bash
# Clone the repo
git clone https://github.com/Jhonniek/aurora.git

# Run locally with dev config
docker compose -f compose.dev.yaml up
```

---

## Key results

- **~90 s deployment cycle** — from `git push` to live container, fully automated
- **0 manual steps** after initial server setup — no SSH, no manual pulls, no restarts
- **Zero credential exposure** — all secrets managed via GitHub Secrets and server-side `.env`; nothing hardcoded in source or logs
- **Reproducible environment** — multi-stage Docker image and locked dependencies (`uv.lock`) ensure dev and prod behave identically

---

## What I learned

Building this pipeline required connecting several systems that don't come pre-wired together: configuring OCI network security rules to allow GitHub Actions runners through, setting up GHCR authentication from a workflow, and chaining SCP + SSH steps in the right order so the compose file is updated before the container restarts. The biggest challenge was debugging SSH connectivity between GitHub-hosted runners and OCI — the fix was opening the correct ingress port in the OCI security list and using a correctly scoped SSH key.

---

*Part of a broader infrastructure project. See also: [OCI Terraform provisioning repo](#) | [Portfolio](#)*
