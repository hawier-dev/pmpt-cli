#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="pmpt"
REPO_URL="https://github.com/hawier-dev/pmpt-cli.git"
INSTALL_DIR="$HOME/.local/share/$APP_NAME"
BIN_DIR="$HOME/.local/bin"
WRAPPER_SCRIPT="$BIN_DIR/$APP_NAME"

echo -e "${BLUE}Installing PMPT CLI...${NC}"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo -e "${RED}Error: Python 3.8+ is required. Found: $PYTHON_VERSION${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"

# Create directories
mkdir -p "$BIN_DIR"
mkdir -p "$(dirname "$INSTALL_DIR")"

# Remove existing installation
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}Removing existing installation...${NC}"
    rm -rf "$INSTALL_DIR"
fi

# Clone repository
echo -e "${BLUE}Cloning repository...${NC}"
git clone "$REPO_URL" "$INSTALL_DIR"

# Create virtual environment
echo -e "${BLUE}Creating virtual environment...${NC}"
cd "$INSTALL_DIR"
python3 -m venv venv

# Activate virtual environment and install
echo -e "${BLUE}Installing dependencies...${NC}"
source venv/bin/activate
pip install --upgrade pip
pip install -e .

# Create wrapper script
echo -e "${BLUE}Creating wrapper script...${NC}"
cat > "$WRAPPER_SCRIPT" << EOF
#!/bin/bash
source "$INSTALL_DIR/venv/bin/activate"
exec python "$INSTALL_DIR/pmpt_main.py" "\$@"
EOF

chmod +x "$WRAPPER_SCRIPT"

# Add to PATH if needed
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo -e "${YELLOW}Adding $BIN_DIR to PATH...${NC}"
    
    # Detect shell and add to appropriate config file
    if [ -n "$ZSH_VERSION" ]; then
        SHELL_CONFIG="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        SHELL_CONFIG="$HOME/.bashrc"
    else
        SHELL_CONFIG="$HOME/.profile"
    fi
    
    echo "export PATH=\"\$PATH:$BIN_DIR\"" >> "$SHELL_CONFIG"
    export PATH="$PATH:$BIN_DIR"
    
    echo -e "${YELLOW}Please restart your shell or run: source $SHELL_CONFIG${NC}"
fi

echo -e "${GREEN}✓ PMPT CLI installed successfully!${NC}"
echo -e "${BLUE}Usage: $APP_NAME${NC}"
echo -e "${BLUE}First run will guide you through configuration.${NC}"