#!/bin/bash
# 🚀 MASTER DEPLOYMENT ORCHESTRATOR
# One script to handle GitHub + HF Spaces + Local deployment

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                                                               ║"
echo "║    🚀 AI RESEARCH ASSISTANT - DEPLOYMENT ORCHESTRATOR 🚀      ║"
echo "║                                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Function to print menu
print_menu() {
    echo ""
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║           CHOOSE YOUR DEPLOYMENT OPTION                       ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo ""
    echo "1️⃣  GitHub Only (Code Backup)"
    echo "   └─ Create GitHub repo, push code"
    echo "   └─ Time: ~5 minutes"
    echo ""
    echo "2️⃣  HF Spaces Only (Live Public App)"
    echo "   └─ Deploy to Hugging Face Spaces"
    echo "   └─ Time: ~10 minutes (5 min build)"
    echo ""
    echo "3️⃣  Local Network Only (Fastest Demo)"
    echo "   └─ Run docker-compose, get network URL"
    echo "   └─ Time: ~1 minute"
    echo ""
    echo "4️⃣  GitHub + HF Spaces (Recommended)"
    echo "   └─ Push to both platforms"
    echo "   └─ Time: ~10 minutes"
    echo ""
    echo "5️⃣  All Three (Professional Setup) ⭐"
    echo "   └─ GitHub + HF Spaces + Local"
    echo "   └─ Time: ~15 minutes"
    echo ""
    echo "0️⃣  Just Show Me Commands (Read-Only)"
    echo "   └─ Display all commands without running"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Function for GitHub deployment
deploy_github() {
    echo ""
    echo "📦 GITHUB DEPLOYMENT"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "1. Create GitHub repo at: https://github.com/new"
    echo "   Name: ai-research-assistant"
    echo "   Public"
    echo ""
    echo "2. Get GitHub token: https://github.com/settings/tokens"
    echo "   Scope: repo"
    echo ""
    echo "3. Copy the repo URL shown after creation"
    echo ""
    read -p "Enter your GitHub repo URL (https://github.com/...): " github_url
    
    if [ -z "$github_url" ]; then
        echo "❌ No URL provided."
        return 1
    fi
    
    cd /Users/amshumathshetty/Desktop/ai-research-assistant
    
    # Remove origin if exists
    git remote remove origin 2>/dev/null
    
    # Add GitHub remote
    git remote add origin "$github_url"
    
    echo ""
    echo "📤 Pushing to GitHub..."
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo "✅ GitHub push successful!"
        echo "📍 Your repo: $github_url"
        return 0
    else
        echo "❌ GitHub push failed"
        return 1
    fi
}

# Function for HF Spaces deployment
deploy_hf_spaces() {
    echo ""
    echo "🤖 HUGGING FACE SPACES DEPLOYMENT"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "HF Spaces remote already configured!"
    echo "📍 Your Space: https://huggingface.co/spaces/nachikethshetty/ai-research-assistant-openenv"
    echo ""
    echo "📤 Pushing to HF Spaces..."
    echo ""
    
    cd /Users/amshumathshetty/Desktop/ai-research-assistant
    git push hf main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ HF Spaces push successful!"
        echo "⏳ Building (2-5 minutes)..."
        echo "🔗 Your live URL:"
        echo "   https://huggingface.co/spaces/nachikethshetty/ai-research-assistant-openenv"
        echo ""
        echo "💡 Pro Tip: Add GOOGLE_API_KEY to Space secrets:"
        echo "   1. Go to Space Settings"
        echo "   2. Repository secrets"
        echo "   3. Add GOOGLE_API_KEY from https://makersuite.google.com"
        return 0
    else
        echo "❌ HF Spaces push failed"
        return 1
    fi
}

# Function for local deployment
deploy_local() {
    echo ""
    echo "🐳 LOCAL DOCKER DEPLOYMENT"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    cd /Users/amshumathshetty/Desktop/ai-research-assistant
    
    echo "🚀 Starting Docker..."
    docker-compose up -d
    
    if [ $? -eq 0 ]; then
        sleep 3
        echo "✅ Docker started successfully!"
        echo ""
        echo "📍 Getting your network IP..."
        ip=$(ifconfig getifaddr en0)
        
        if [ -z "$ip" ]; then
            echo "⚠️  Could not auto-detect IP. Run manually:"
            echo "   ifconfig getifaddr en0"
        else
            echo "✅ Your IP: $ip"
            echo ""
            echo "🌐 Share this URL:"
            echo "   http://$ip:8501"
            echo ""
            echo "⏱️  App starting... (30 seconds)"
        fi
        return 0
    else
        echo "❌ Docker start failed"
        return 1
    fi
}

# Function to show all commands
show_commands() {
    echo ""
    echo "📋 ALL DEPLOYMENT COMMANDS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "GITHUB:"
    echo "  git remote add origin https://github.com/YOUR_USERNAME/ai-research-assistant"
    echo "  git push -u origin main"
    echo ""
    echo "HF SPACES:"
    echo "  git push hf main"
    echo ""
    echo "LOCAL:"
    echo "  docker-compose up -d"
    echo "  ifconfig getifaddr en0"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Main menu loop
while true; do
    print_menu
    read -p "Choose option (0-5): " choice
    
    case $choice in
        1)
            deploy_github
            ;;
        2)
            deploy_hf_spaces
            ;;
        3)
            deploy_local
            ;;
        4)
            deploy_github && deploy_hf_spaces
            ;;
        5)
            deploy_github && deploy_hf_spaces && deploy_local
            ;;
        0)
            show_commands
            break
            ;;
        *)
            echo "❌ Invalid option"
            ;;
    esac
    
    echo ""
    read -p "Do you want to continue? (y/n): " continue
    if [ "$continue" != "y" ]; then
        break
    fi
done

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                  DEPLOYMENT COMPLETE! 🎉                      ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "📖 For more details, read:"
echo "   DEPLOYMENT_FINAL_SUMMARY.md"
echo "   QUICK_COMMANDS.md"
echo "   GITHUB_AND_DEPLOYMENT.md"
echo ""
