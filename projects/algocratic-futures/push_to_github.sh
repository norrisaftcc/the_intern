#!/bin/bash
#
# Push local secrets to GitHub repository
# Requires GitHub CLI (gh) to be authenticated
#

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║           PUSH SECRETS TO GITHUB REPOSITORY                   ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo "❌ .env.local not found. Run ./setup_secrets.sh first!"
    exit 1
fi

# Load the environment variables
source .env.local

# Check if gh is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed."
    echo "Install it from: https://cli.github.com/"
    exit 1
fi

# Check if gh is authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ GitHub CLI is not authenticated."
    echo "Run: gh auth login"
    exit 1
fi

echo "This will add your API keys to the repository secrets."
echo "Repository: norrisaftcc/the_intern"
echo ""
echo "Keys to push:"
[ ! -z "$CLAUDE_API_KEY" ] && echo "  ✓ CLAUDE_API_KEY (required for AI code reviews)"
[ ! -z "$OPENAI_API_KEY" ] && echo "  ✓ OPENAI_API_KEY"
[ ! -z "$GEMINI_API_KEY" ] && echo "  ✓ GEMINI_API_KEY"
[ ! -z "$GITHUB_TOKEN" ] && echo "  ✓ GITHUB_TOKEN"
echo ""
read -p "Continue? (y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo "Pushing secrets to GitHub..."

# Push each key if it exists
if [ ! -z "$CLAUDE_API_KEY" ]; then
    echo -n "Setting CLAUDE_API_KEY... "
    if gh secret set CLAUDE_API_KEY --body "$CLAUDE_API_KEY" -R norrisaftcc/the_intern 2>/dev/null; then
        echo "✓"
    else
        echo "❌ Failed (may already exist or permission denied)"
    fi
fi

if [ ! -z "$OPENAI_API_KEY" ]; then
    echo -n "Setting OPENAI_API_KEY... "
    if gh secret set OPENAI_API_KEY --body "$OPENAI_API_KEY" -R norrisaftcc/the_intern 2>/dev/null; then
        echo "✓"
    else
        echo "❌ Failed"
    fi
fi

if [ ! -z "$GEMINI_API_KEY" ]; then
    echo -n "Setting GEMINI_API_KEY... "
    if gh secret set GEMINI_API_KEY --body "$GEMINI_API_KEY" -R norrisaftcc/the_intern 2>/dev/null; then
        echo "✓"
    else
        echo "❌ Failed"
    fi
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                    GITHUB SECRETS UPDATED! 🚀                 ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "Your AI code review workflow should now work!"
echo ""
echo "To test:"
echo "  1. Create a new PR or push to existing PR"
echo "  2. Check Actions tab for workflow execution"
echo "  3. Look for AI review comment on the PR"
echo ""
echo "To verify secrets are set:"
echo "  gh secret list -R norrisaftcc/the_intern"