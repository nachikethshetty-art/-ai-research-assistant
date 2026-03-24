#!/bin/bash
# 🚀 AUTOMATED GITHUB SETUP & PUSH SCRIPT

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         🚀 AI RESEARCH ASSISTANT - GITHUB SETUP                ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

echo "This script will help you push your code to GitHub."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if origin remote already exists
if git remote get-url origin &>/dev/null; then
    echo "ℹ️  Origin remote already exists:"
    git remote get-url origin
    echo ""
    read -p "Do you want to change it? (y/n): " change_remote
else
    change_remote="y"
fi

if [ "$change_remote" = "y" ]; then
    echo "📝 Enter your GitHub repository URL"
    echo "   Format: https://github.com/USERNAME/ai-research-assistant"
    echo ""
    read -p "GitHub URL: " github_url
    
    if [ -z "$github_url" ]; then
        echo "❌ No URL provided. Exiting."
        exit 1
    fi
    
    # Remove existing origin if it exists
    git remote remove origin 2>/dev/null
    
    # Add new origin
    git remote add origin "$github_url"
    echo "✅ Added GitHub remote"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Current remotes:"
git remote -v
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "📋 Files to be pushed:"
echo ""
git status --short
echo ""

read -p "Ready to push to GitHub? (y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo "❌ Cancelled."
    exit 1
fi

echo ""
echo "🔐 AUTHENTICATION:"
echo ""
echo "When git asks for credentials, use one of these:"
echo ""
echo "1️⃣  GitHub Personal Access Token (recommended):"
echo "   • Go to: https://github.com/settings/tokens"
echo "   • Click 'Generate new token'"
echo "   • Scope: repo"
echo "   • Copy token and paste when prompted"
echo ""
echo "2️⃣  GitHub Username + Password (if token not set up):"
echo "   • Use your GitHub login credentials"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "🚀 Pushing to GitHub..."
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║                   ✅ PUSH SUCCESSFUL! ✅                       ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "🎉 Your code is now on GitHub!"
    echo ""
    echo "📍 Your GitHub URL:"
    echo "   $(git remote get-url origin)"
    echo ""
    echo "💡 Next steps:"
    echo "   1. Visit your GitHub repo above"
    echo "   2. Add topics (ai-research, hackathon, rag, etc.)"
    echo "   3. Share the link with your team/judges"
    echo ""
    echo "🔗 You now have:"
    echo "   • GitHub: $(git remote get-url origin)"
    echo "   • HF Spaces: https://huggingface.co/spaces/nachikethshetty/ai-research-assistant-openenv"
    echo "   • Local: docker-compose up -d → http://YOUR_IP:8501"
    echo ""
else
    echo ""
    echo "❌ Push failed!"
    echo ""
    echo "🔧 Troubleshooting:"
    echo "   • Check your GitHub URL is correct"
    echo "   • Check your GitHub credentials/token"
    echo "   • Make sure repo exists at:"
    echo "     $(git remote get-url origin)"
    echo ""
    echo "Try again with:"
    echo "   git push -u origin main"
    echo ""
fi
