# Azure Deployment Guide - AI Research Assistant with Groq

## Prerequisites
- Azure account (free tier from GitHub Student Pack)
- Docker installed locally
- Git installed
- Your Groq API key

---

## Step 1: Set Up Azure Account

1. Go to: https://azure.microsoft.com/en-us/free/students/
2. Sign in with GitHub account
3. Activate $100+ in free credits
4. Create a resource group:
   ```bash
   az group create --name research-assistant --location eastus
   ```

---

## Step 2: Build Docker Image Locally

```bash
cd /Users/amshumathshetty/Desktop/ai-research-assistant

# Build the Docker image
docker build -f server/Dockerfile -t research-assistant:latest .

# Test locally
docker run -p 8501:8501 \
  -e GROQ_API_KEY=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 \
  research-assistant:latest

# Open http://localhost:8501 to test
```

---

## Step 3: Push to Azure Container Registry (ACR)

1. Create a container registry:
   ```bash
   az acr create --resource-group research-assistant \
     --name researchassistant \
     --sku Basic
   ```

2. Get login credentials:
   ```bash
   az acr credential show --resource-group research-assistant \
     --name researchassistant
   ```

3. Login and push:
   ```bash
   az acr login --name researchassistant
   
   docker tag research-assistant:latest \
     researchassistant.azurecr.io/research-assistant:latest
   
   docker push researchassistant.azurecr.io/research-assistant:latest
   ```

---

## Step 4: Deploy to Azure Container Instances

```bash
az container create \
  --resource-group research-assistant \
  --name research-assistant-app \
  --image researchassistant.azurecr.io/research-assistant:latest \
  --registry-login-server researchassistant.azurecr.io \
  --registry-username <USERNAME> \
  --registry-password <PASSWORD> \
  --environment-variables \
    GROQ_API_KEY=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 \
  --ports 8501 \
  --ip-address public
```

---

## Step 5: Get the Public URL

```bash
az container show --resource-group research-assistant \
  --name research-assistant-app \
  --query ipAddress.fqdn
```

**Your app will be live at**: `http://<FQDN>:8501`

---

## Alternative: Deploy to Azure App Service

1. Create App Service plan:
   ```bash
   az appservice plan create \
     --name research-assistant-plan \
     --resource-group research-assistant \
     --sku B1 \
     --is-linux
   ```

2. Deploy:
   ```bash
   az webapp create \
     --name research-assistant-app \
     --resource-group research-assistant \
     --plan research-assistant-plan \
     --deployment-container-image-name \
       researchassistant.azurecr.io/research-assistant:latest
   ```

3. Configure environment variables:
   ```bash
   az webapp config appsettings set \
     --name research-assistant-app \
     --resource-group research-assistant \
     --settings GROQ_API_KEY=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
   ```

---

## Cost Estimation

| Resource | Cost | Notes |
|----------|------|-------|
| Container Registry | Free tier | 1 free registry |
| Container Instances | ~$0.0015/hour | Only when running |
| Data Transfer | ~$0.12/GB | Usually minimal |
| **Monthly (24/7)** | ~$11 | Well within free tier |

---

## Monitoring

View logs:
```bash
az container logs --resource-group research-assistant \
  --name research-assistant-app
```

Check status:
```bash
az container show --resource-group research-assistant \
  --name research-assistant-app \
  --query instanceView.state
```

---

## Cleanup (Optional)

To delete and save costs:
```bash
az group delete --name research-assistant --yes
```

---

## Troubleshooting

### App won't start?
Check logs: `az container logs --resource-group research-assistant --name research-assistant-app`

### Groq API key error?
Verify environment variable is set correctly in Azure

### Slow response?
This is normal - Groq API takes 1-5 seconds per query

---

**Your live app is now running on Azure!** 🎉
