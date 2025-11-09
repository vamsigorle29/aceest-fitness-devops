#!/bin/bash
# Quick SonarQube Setup Script
# This script helps you set up SonarQube with SonarCloud (FREE)

echo "🚀 SonarQube Setup Helper"
echo "=========================="
echo ""

# Check if running in GitHub Actions
if [ -n "$GITHUB_ACTIONS" ]; then
    echo "ℹ️  Running in GitHub Actions"
    echo "To set up SonarQube:"
    echo "1. Go to https://sonarcloud.io"
    echo "2. Sign up with GitHub"
    echo "3. Create a project for this repository"
    echo "4. Get your token and add it as SONAR_TOKEN secret"
    exit 0
fi

echo "This script will guide you through setting up SonarCloud (FREE)"
echo ""

# Check if gh CLI is installed
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI detected"
    echo ""
    echo "Would you like to:"
    echo "1. Open SonarCloud signup page"
    echo "2. Open GitHub secrets page"
    echo "3. Just show instructions"
    read -p "Choose option (1-3): " choice
    
    case $choice in
        1)
            echo "Opening SonarCloud..."
            if [[ "$OSTYPE" == "darwin"* ]]; then
                open "https://sonarcloud.io/signup"
            elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
                xdg-open "https://sonarcloud.io/signup"
            else
                echo "Please visit: https://sonarcloud.io/signup"
            fi
            ;;
        2)
            echo "Opening GitHub secrets page..."
            REPO=$(git config --get remote.origin.url | sed 's/.*github.com[:/]\(.*\)\.git/\1/')
            if [[ "$OSTYPE" == "darwin"* ]]; then
                open "https://github.com/$REPO/settings/secrets/actions"
            elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
                xdg-open "https://github.com/$REPO/settings/secrets/actions"
            else
                echo "Please visit: https://github.com/$REPO/settings/secrets/actions"
            fi
            ;;
    esac
fi

echo ""
echo "📝 Step-by-Step Instructions:"
echo ""
echo "1. Go to https://sonarcloud.io"
echo "2. Click 'Log in' → 'Log in with GitHub'"
echo "3. Authorize SonarCloud"
echo "4. Click '+' → 'Analyze new project'"
echo "5. Select 'From GitHub' → Choose this repository"
echo "6. Click 'Set up' → Choose 'Free' → 'Create project'"
echo "7. Go to: Account → My Account → Security"
echo "8. Generate a token (name it 'GitHub Actions')"
echo "9. Copy the token"
echo "10. Go to GitHub: Repository → Settings → Secrets → Actions"
echo "11. Click 'New repository secret'"
echo "12. Name: SONAR_TOKEN"
echo "13. Value: [Paste your token]"
echo "14. Click 'Add secret'"
echo ""
echo "✅ Done! SonarQube will run automatically on the next push."
echo ""

