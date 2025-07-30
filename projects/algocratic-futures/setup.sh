#!/bin/bash
#
# AlgoCratic Futures - Automated Setup Script
# Sets up virtual environment and installs dependencies
#

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║           ALGOCRATIC FUTURES - AUTOMATED SETUP                ║"
echo "║                                                               ║"
echo "║  Setting up your assessment environment...                    ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Removing old one..."
    rm -rf venv
fi

python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing requirements..."
cd backend
pip install -r requirements.txt
cd ..

# Create necessary directories
echo ""
echo "Creating directory structure..."
mkdir -p logs
mkdir -p data
mkdir -p agents/custom

# Test imports
echo ""
echo "Testing core imports..."
python3 -c "import fastapi; import adventurelib; import yaml; print('✓ All core modules imported successfully')"

# Create activation helper
echo ""
echo "Creating activation helper..."
cat > activate.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
echo "✓ AlgoCratic Futures environment activated"
echo "Run 'python launch_mvp.py' to start"
EOF
chmod +x activate.sh

# Success message
echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                    SETUP COMPLETE! ✨                         ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "To start using AlgoCratic Futures:"
echo ""
echo "1. Activate the environment:"
echo "   source venv/bin/activate"
echo "   (or use ./activate.sh)"
echo ""
echo "2. Launch the game:"
echo "   python launch_mvp.py"
echo ""
echo "3. Choose your experience:"
echo "   - Option 1: Arcade tutorial (adventurelib)"
echo "   - Option 2: Full MUD with Liza (room system)"
echo "   - Option 3: Web interface"
echo "   - Option 4: Everything!"
echo ""
echo "Happy assessment! Remember: Your productivity is being monitored. 👁️"