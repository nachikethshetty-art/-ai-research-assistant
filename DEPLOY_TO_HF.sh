#!/bin/bash
# 🚀 FINAL DEPLOYMENT SCRIPT
# Run this to push your app to HF Spaces

echo "🔐 You need to authenticate with Hugging Face..."
echo ""
echo "INSTRUCTIONS:"
echo "1. Visit: https://huggingface.co/settings/tokens"
echo "2. Create NEW TOKEN (Read + Write access)"
echo "3. Copy the token"
echo "4. When prompted, paste the token and press Enter"
echo ""
echo "Then the deployment will complete in 30-60 seconds!"
echo ""

cd /Users/amshumathshetty/Desktop/ai-research-assistant

# Git push with HF authentication
git push hf main

if [ $? -eq 0 ]; then
    echo "✅ DEPLOYMENT SUCCESSFUL!"
    echo ""
    echo "🎉 Your app is now live at:"
    echo "https://huggingface.co/spaces/nachikethshetty/ai-research-assistant-openenv"
    echo ""
    echo "⏳ HF will build in 2-5 minutes. Check back soon!"
    echo ""
    echo "📖 Read HF_SPACES_DEPLOYMENT.md for full details"
else
    echo "❌ Deployment failed. Check your HF token."
    echo "Get a new token: https://huggingface.co/settings/tokens"
fi
