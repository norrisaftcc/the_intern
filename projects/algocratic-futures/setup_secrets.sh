#!/bin/bash
#
# Safe API Key Setup Script
# This keeps your keys local and out of git
#

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║           ALGOCRATIC FUTURES - SECRET SETUP                   ║"
echo "║                                                               ║"
echo "║  This script helps you safely configure API keys              ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Check if .env.local exists
if [ -f ".env.local" ]; then
    echo "⚠️  .env.local already exists. Loading existing configuration..."
    source .env.local
    echo "✓ Loaded existing environment variables"
    echo ""
fi

# Function to safely read API key
read_api_key() {
    local key_name=$1
    local key_description=$2
    
    echo "Enter your $key_description:"
    echo "(Input will be hidden for security)"
    read -s api_key
    echo ""
    
    if [ -z "$api_key" ]; then
        echo "❌ No key entered. Skipping $key_name"
        return 1
    fi
    
    # Validate key format (basic check)
    if [[ ${#api_key} -lt 20 ]]; then
        echo "⚠️  Warning: Key seems too short. Are you sure it's correct?"
        read -p "Continue anyway? (y/n): " confirm
        if [ "$confirm" != "y" ]; then
            return 1
        fi
    fi
    
    # Save to .env.local
    echo "export $key_name='$api_key'" >> .env.local
    echo "✓ $key_name saved to .env.local"
    return 0
}

# Menu for different keys
echo "Which API key would you like to configure?"
echo ""
echo "1. Claude API Key (for AI code reviews)"
echo "2. OpenAI API Key (optional, for GPT models)"
echo "3. Gemini API Key (optional, for Google models)"
echo "4. GitHub Token (for enhanced GitHub operations)"
echo "5. All of the above"
echo "0. Exit"
echo ""
read -p "Select option (0-5): " choice

case $choice in
    1)
        read_api_key "CLAUDE_API_KEY" "Claude API Key"
        ;;
    2)
        read_api_key "OPENAI_API_KEY" "OpenAI API Key"
        ;;
    3)
        read_api_key "GEMINI_API_KEY" "Gemini API Key"
        ;;
    4)
        read_api_key "GITHUB_TOKEN" "GitHub Personal Access Token"
        ;;
    5)
        read_api_key "CLAUDE_API_KEY" "Claude API Key"
        read_api_key "OPENAI_API_KEY" "OpenAI API Key"
        read_api_key "GEMINI_API_KEY" "Gemini API Key"
        read_api_key "GITHUB_TOKEN" "GitHub Personal Access Token"
        ;;
    0)
        echo "Exiting without changes."
        exit 0
        ;;
    *)
        echo "Invalid option. Exiting."
        exit 1
        ;;
esac

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                    SETUP COMPLETE! 🔐                         ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "Your API keys are stored in .env.local (git-ignored)"
echo ""
echo "To use these keys:"
echo "  source .env.local"
echo ""
echo "To add to GitHub repository secrets (for CI/CD):"
echo "  gh secret set CLAUDE_API_KEY --body \"\$CLAUDE_API_KEY\""
echo ""
echo "To test locally with the keys:"
echo "  python backend/test_with_keys.py"
echo ""
echo "Remember: NEVER commit .env.local to git!"