#!/bin/bash
# Git repository setup script
# Run this script to initialize the repository and create the benjamin-solution branch

set -e

echo "Setting up git repository..."

# Initialize git repository (if not already initialized)
if [ ! -d .git ]; then
    git init
    echo "Git repository initialized"
else
    echo "Git repository already initialized"
fi

# Create and switch to benjamin-solution branch
git checkout -b benjamin-solution 2>/dev/null || git checkout benjamin-solution

# Add all files
git add .

# Show status
echo ""
echo "Repository setup complete!"
echo "Current branch: $(git branch --show-current)"
echo ""
echo "To commit and push:"
echo "  git commit -m 'Initial commit: Production-ready DevOps solution'"
echo "  git remote add origin <your-github-repo-url>"
echo "  git push -u origin benjamin-solution"
