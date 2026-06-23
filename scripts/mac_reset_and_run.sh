#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/millerjaytee-star/concrete-motivation-ai.git"
PROJECT_DIR="$HOME/concrete-motivation-ai"

echo "========================================"
echo " Concrete Motivation AI - Mac Launcher"
echo "========================================"
echo

if ! command -v git >/dev/null 2>&1; then
  echo "Git is not installed. Install Xcode Command Line Tools first:"
  echo "xcode-select --install"
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is not installed. Install Python 3 first."
  exit 1
fi

if [ -d "$PROJECT_DIR/.git" ]; then
  echo "Found existing project at: $PROJECT_DIR"
  cd "$PROJECT_DIR"
  echo "Resetting local files to match GitHub main..."
  git fetch origin
  git reset --hard origin/main
else
  echo "Cloning fresh project into: $PROJECT_DIR"
  rm -rf "$PROJECT_DIR"
  git clone "$REPO_URL" "$PROJECT_DIR"
  cd "$PROJECT_DIR"
fi

echo
echo "Project ready. Starting Concrete Motivation AI..."
echo
python3 main.py
