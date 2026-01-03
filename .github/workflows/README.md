# 🚀 CI/CD Pipeline Documentation

## Overview

This repository uses a **unified, production-ready CI/CD pipeline** that handles:

- ✅ Code quality checks (pre-commit)
- ✅ Security scanning (Trivy)
- ✅ Automated testing (Backend + Frontend)
- ✅ Docker image building & publishing
- ✅ Automatic deployment to Liara (optional)

---

## 📊 Pipeline Architecture

```mermaid
graph LR
    A[Push to main/PR] --> B[🛡️ Quality & Security]
    B --> C[🐍 Backend Tests]
    B --> D[⚛️ Frontend Tests]
    C --> E[🐳 Docker Build]
    D --> E
    E --> F[🚀 Deploy to Liara]
    F --> G[✅ Production]
```

---

## 📂 Pipeline Stages

### Stage 1: Quality & Security Checks 🛡️

**Purpose:** Ensure code quality and security before running tests.

**Steps:**
1. **Pre-commit hooks:**
   - Code formatting (Black, Prettier)
   - Linting (Flake8, ESLint)
   - Type checking
   - Trailing whitespace removal

2. **Trivy Security Scan:**
   - Scans for vulnerabilities (CRITICAL, HIGH, MEDIUM)
   - Checks dependencies for known CVEs
   - Reports security issues (non-blocking)

**Duration:** ~1-2 minutes

**Cache Used:** ✅ Pre-commit cache

---

### Stage 2: Backend Tests 🐍

**Purpose:** Validate Django backend functionality.

**Services:**
- PostgreSQL 15 (Alpine)
- Redis 7 (Alpine)

**Steps:**
1. Install Python dependencies
2. Wait for database health check
3. Run migrations
4. Execute Django tests with coverage
5. Generate coverage report (HTML)

**Test Settings:**
- `DJANGO_SETTINGS_MODULE=config.settings.test`
- Fast password hashing (MD5)
- Eager Celery tasks (synchronous)
- In-memory operations where possible

**Coverage Report:**
- Uploaded as artifact (7-day retention)
- Available in Actions tab

**Duration:** ~3-5 minutes

**Cache Used:** ✅ pip cache

---

### Stage 3: Frontend Tests ⚛️

**Purpose:** Build and validate React frontend.

**Steps:**
1. Install Node.js dependencies (npm ci)
2. Build production bundle
3. Check bundle size

**Duration:** ~2-3 minutes

**Cache Used:** ✅ npm cache

---

### Stage 4: Docker Build & Push 🐳

**Purpose:** Build and publish Docker images.

**Trigger:** Only on `push` to `main` branch

**Images Built:**
1. **Backend Image:**
   - `ghcr.io/mhmdrz22/enginner/backend:latest`
   - `ghcr.io/mhmdrz22/enginner/backend:<sha>`

2. **Frontend Image:**
   - `ghcr.io/mhmdrz22/enginner/frontend:latest`
   - `ghcr.io/mhmdrz22/enginner/frontend:<sha>`

**Features:**
- Multi-layer caching (GitHub Actions cache)
- OCI labels (source, revision)
- Automatic tagging (latest + commit SHA)

**Duration:** ~5-10 minutes (with cache)

**Cache Used:** ✅ Docker BuildKit cache

---

### Stage 5: Deploy to Liara 🚀

**Purpose:** Automatic deployment to Liara PaaS.

**Trigger:** Only when:
- `push` to `main` branch
- Previous stages passed
- `LIARA_API_TOKEN` secret is set

**Steps:**
1. Install Liara CLI
2. Deploy application
3. Report deployment URL

**Duration:** ~2-3 minutes

**Configuration Required:**
- GitHub Secret: `LIARA_API_TOKEN`
- Environment variable: `LIARA_APP_NAME`

---

### Stage 6: Pipeline Summary 📋

**Purpose:** Generate human-readable summary.

**Features:**
- Job status table
- Success/failure indicators
- Deployment information
- Available in Actions Summary tab

---

## ⚙️ Configuration

### Required Secrets

Add these secrets in **Settings → Secrets and variables → Actions**:

| Secret | Required For | How to Get |
|--------|--------------|------------|
| `LIARA_API_TOKEN` | Liara deployment | [Liara Dashboard](https://console.liara.ir/api-tokens) |
| `GITHUB_TOKEN` | Docker push | Auto-generated (no action needed) |

### Environment Variables

Configured in `production-pipeline.yml`:

```yaml
env:
  REGISTRY: ghcr.io                    # GitHub Container Registry
  IMAGE_NAME: ${{ github.repository }} # Auto: mhmdrz22/enginner
  LIARA_APP_NAME: enginner-taskboard   # Your Liara app name
  PYTHON_VERSION: '3.11'               # Python version
  NODE_VERSION: '18'                   # Node.js version
```

---

## 🛠️ Maintenance

### Updating Dependencies

**Python:**
```bash
cd backend
pip install <package>
pip freeze > requirements.txt
git commit -am "deps: update Python dependencies"
```

**Node.js:**
```bash
cd frontend
npm install <package>
git commit -am "deps: update Node dependencies"
```

### Upgrading GitHub Actions

Check for updates:
```bash
# Check current versions
grep 'uses:' .github/workflows/production-pipeline.yml

# Update to latest:
# actions/checkout@v4 -> actions/checkout@v5 (when available)
```

---

## 📊 Performance Metrics

### Average Pipeline Duration

| Stage | Duration | Cache Hit | Cache Miss |
|-------|----------|-----------|------------|
| Quality Checks | 1-2 min | 1 min | 2 min |
| Backend Tests | 3-5 min | 3 min | 5 min |
| Frontend Tests | 2-3 min | 2 min | 3 min |
| Docker Build | 5-10 min | 5 min | 10 min |
| Deploy | 2-3 min | N/A | N/A |
| **Total** | **13-23 min** | **13 min** | **23 min** |

### Resource Usage

- **GitHub Actions Minutes:** ~15-20 minutes per run
- **Storage:** ~500MB (Docker cache + artifacts)
- **Retention:** 7 days (coverage reports)

---

## 🐛 Troubleshooting

### Pipeline Fails at Quality Checks

**Problem:** Pre-commit hooks fail

**Solution:**
```bash
# Run pre-commit locally before pushing:
pre-commit install
pre-commit run --all-files

# Auto-fix issues:
pre-commit run --all-files --hook-stage manual
git add -u
git commit -m "style: fix pre-commit issues"
```

---

### Backend Tests Fail

**Problem:** Database connection errors

**Check:**
1. PostgreSQL health check passed?
2. Migrations applied successfully?
3. Environment variables correct?

**Debug Locally:**
```bash
# Run tests locally with same setup:
docker-compose up -d db redis
export DATABASE_URL=postgresql://test_user:test_password@localhost:5432/test_db
cd backend
python manage.py test
```

---

### Docker Build Fails

**Problem:** Image build errors

**Common Causes:**
1. `requirements.txt` has invalid package
2. Dockerfile syntax error
3. Build context too large

**Solution:**
```bash
# Test Docker build locally:
cd backend
docker build -t test-backend .

# Check build context size:
du -sh .

# Verify .dockerignore excludes unnecessary files
```

---

### Liara Deployment Fails

**Problem:** Deployment errors

**Check:**
1. `LIARA_API_TOKEN` secret is set?
2. `LIARA_APP_NAME` is correct?
3. Liara app exists and is configured?

**Manual Deploy:**
```bash
# Test deployment manually:
npm install -g @liara/cli
liara login
liara deploy --app enginner-taskboard
```

---

## 🔒 Security Best Practices

### ✅ Implemented

- [x] Secrets stored in GitHub Secrets (not in code)
- [x] Non-root Docker user
- [x] Trivy security scanning
- [x] Dependency vulnerability checks
- [x] Minimal base images (Alpine)
- [x] No hardcoded credentials
- [x] HTTPS-only in production

### 🛡️ Additional Recommendations

- [ ] Enable Dependabot for automatic dependency updates
- [ ] Add CodeQL for code scanning
- [ ] Implement branch protection rules
- [ ] Require signed commits
- [ ] Enable 2FA for all collaborators

---

## 📝 Workflow File Structure

```
.github/workflows/
├── production-pipeline.yml       # Main unified pipeline
├── README.md                     # This documentation
└── .deprecated/                  # Archived old workflows
    ├── ci-cd.yml.old
    └── deploy.yml.old
```

---

## 🎯 Performance Optimization

### Caching Strategy

**What's Cached:**
1. Pre-commit hooks (`~/.cache/pre-commit`)
2. pip packages (`~/.cache/pip`)
3. npm packages (`~/.npm`)
4. Docker layers (GitHub Actions cache)

**Cache Hit Rate:** ~80-90%

**Cache Size:** ~200-300MB per repository

### Parallelization

**Jobs Running in Parallel:**
- Backend Tests + Frontend Tests (after Quality Checks)
- Total time saved: ~3-5 minutes per run

---

## 📊 Monitoring & Alerts

### GitHub Actions Status Badge

Add to `README.md`:

```markdown
[![CI/CD Pipeline](https://github.com/mhmdrz22/enginner/actions/workflows/production-pipeline.yml/badge.svg)](https://github.com/mhmdrz22/enginner/actions/workflows/production-pipeline.yml)
```

### Notification Settings

**GitHub:**
- Settings → Notifications → Actions
- Enable: "Failed workflows only"

**Email Alerts:**
- Automatic for failed runs on `main` branch

---

## 📚 References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [Trivy Security Scanner](https://github.com/aquasecurity/trivy-action)
- [Liara CLI Documentation](https://docs.liara.ir/cli/install/)
- [Pre-commit Framework](https://pre-commit.com/)

---

## ✅ Checklist for New Contributors

Before submitting a PR:

- [ ] Run `pre-commit run --all-files` locally
- [ ] Run `python manage.py test` successfully
- [ ] Run `npm run build` successfully
- [ ] Check that all CI checks pass
- [ ] Review pipeline summary in Actions tab

---

## 💬 Support

If you encounter issues:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the Actions logs in GitHub
3. Open an issue with:
   - Pipeline run URL
   - Error logs
   - Steps to reproduce

---

**Last Updated:** January 3, 2026  
**Pipeline Version:** 1.0.0  
**Maintainer:** [@mhmdrz22](https://github.com/mhmdrz22)
