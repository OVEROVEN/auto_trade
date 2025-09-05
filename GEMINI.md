# AI Trading System - Gemini Assistant Guide

This document provides a comprehensive guide for the Gemini AI assistant to understand, set up, and deploy this project to Google Cloud.

## 📋 Project Overview

This is a full-stack AI-powered stock trading analysis system. 

- **Backend**: A Python/FastAPI server that provides data fetching, technical analysis, AI insights (via OpenAI), and user authentication.
- **Frontend**: A Next.js/TypeScript dashboard for data visualization and user interaction.

## 🏗️ Core Technologies

- **Backend**: Python, FastAPI, Uvicorn
- **Frontend**: Next.js, React, TypeScript, TailwindCSS
- **Testing**: Playwright
- **Containerization**: Docker, Docker Compose
- **Deployment**: Google Cloud Build, Google Cloud Run, Google Artifact Registry

---

## 🚀 Deployment to Google Cloud

This is the primary workflow for deploying the project. It uses a `cloudbuild.yaml` file to ensure a reliable and repeatable process.

### Step 1: Provide Environment Variable Values

To deploy this project, the user **must provide the values** for the following environment variables. The placeholders (`<..._HERE>`) need to be replaced with the actual secrets and configuration values.

**Backend Secrets (for the future; not used in current `cloudbuild.yaml` but good practice):**
- `OPENAI_API_KEY`: `<YOUR_OPENAI_API_KEY_HERE>`
- `DATABASE_URL`: `<YOUR_POSTGRES_DATABASE_URL_HERE>`

**Frontend Build & Runtime Variables:**
- `_NEXT_PUBLIC_API_URL`: `<YOUR_BACKEND_API_URL_HERE>` (e.g., `https://your-backend-service.a.run.app`)
- `_NEXT_PUBLIC_WS_URL`: `<YOUR_BACKEND_WEBSOCKET_URL_HERE>` (e.g., `wss://your-backend-service.a.run.app`)
- `_NEXT_PUBLIC_JWT_SECRET`: `<A_STRONG_RANDOM_SECRET_STRING_HERE>`
- `_NEXT_PUBLIC_GOOGLE_CLIENT_ID`: `<YOUR_GOOGLE_OAUTH_CLIENT_ID_HERE>`
- `_NEXT_PUBLIC_ENVIRONMENT`: `production`
- `_NEXT_PUBLIC_FEATURE_AI_ANALYSIS`: `true`
- `_NEXT_PUBLIC_FEATURE_REDEMPTION`: `true`
- `_NEXT_PUBLIC_FEATURE_TAIWAN_STOCKS`: `true`

**Note:** The `cloudbuild.yaml` is pre-configured to use these variable names with a `_` prefix. The user should provide the values for the assistant to use.

### Step 2: Execute the Deployment

The entire build and deploy process is managed by `cloudbuild.yaml`. The assistant should trigger this build using the `gcloud builds submit` command.

**Deployment Command:**

```bash
gcloud builds submit . --config=cloudbuild.yaml --project=<USER_PROVIDED_PROJECT_ID>
```

**Execution Details:**
- This command should be run from the root of the git repository (`auto_trade/auto_trade`).
- The `cloudbuild.yaml` file already contains the logic to:
  1. Build the frontend Docker image, passing the `_NEXT_PUBLIC_...` variables as build arguments.
  2. Push the image to Google Artifact Registry.
  3. Deploy the new image to the Cloud Run service named `ai-trading-system-frontend`.

This process ensures that the build environment has access to the necessary variables, which was the root cause of previous deployment failures.

---

## ⚙️ Local Development & Verification

To debug or verify changes locally, follow these steps to run the frontend in a production-like mode.

### 1. Install Dependencies
Ensure you are in the `auto_trade` directory.
```bash
npm --prefix frontend ci
```

### 2. Build the Frontend
This step requires the same environment variables as the cloud deployment.

```bash
export NEXT_PUBLIC_API_URL='<BACKEND_URL>' && \
export NEXT_PUBLIC_WS_URL='<WEBSOCKET_URL>' && \
export NEXT_PUBLIC_JWT_SECRET='<JWT_SECRET>' && \
export NEXT_PUBLIC_GOOGLE_CLIENT_ID='<GOOGLE_CLIENT_ID>' && \
export NEXT_PUBLIC_ENVIRONMENT='production' && \
export NEXT_PUBLIC_FEATURE_AI_ANALYSIS='true' && \
export NEXT_PUBLIC_FEATURE_REDEMPTION='true' && \
export NEXT_PUBLIC_FEATURE_TAIWAN_STOCKS='true' && \
npm --prefix frontend run build
```

### 3. Run the Local Production Server
```bash
export NEXT_PUBLIC_API_URL='<BACKEND_URL>' && \
export NEXT_PUBLIC_WS_URL='<WEBSOCKET_URL>' && \
# ... other runtime vars ...
npm --prefix frontend start
```
The server will be available at `http://localhost:3000`.

**Important:** For Google OAuth to work locally, `http://localhost:3000` must be added to the "Authorized JavaScript origins" in the Google Cloud Console for the corresponding OAuth Client ID.

## 🩺 Codebase Status & Known Fixes

This codebase required several fixes to become buildable and deployable. An assistant working on this project should be aware of the following:

1.  **TypeScript Type Errors**: The original code had numerous missing type definitions in `frontend/lib/i18n.ts` and `frontend/contexts/AuthContext.tsx`. These have been fixed. If new build errors of this nature appear, the solution is to find the relevant interface and add the missing property.

2.  **Hardcoded URLs**: The `frontend/contexts/AuthContext.tsx` file contained hardcoded `http://localhost:8000` URLs. These have been replaced to correctly use the `NEXT_PUBLIC_API_URL` environment variable.

3.  **Deployment Method**: The initial approach of using `gcloud run deploy --source` failed because it does not provide build-time environment variables. The correct and now-implemented solution is to use a `cloudbuild.yaml` with `gcloud builds submit`.

4.  **Playwright Dependency**: The `playwright` package was incorrectly listed as a production dependency. It has been moved to `devDependencies`.
