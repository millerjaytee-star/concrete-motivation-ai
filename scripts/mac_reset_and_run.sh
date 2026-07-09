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
  if [ -n "$(git status --porcelain)" ] && [ "${CONFIRM_RESET:-}" != "yes" ]; then
    echo "Local changes are present. Refusing to reset without explicit confirmation."
    echo "Commit or stash your work, or rerun with CONFIRM_RESET=yes if you intentionally want to discard local changes."
    exit 1
  fi
  echo "Updating local files to match GitHub main..."
  git fetch origin
  if [ "${CONFIRM_RESET:-}" = "yes" ]; then
    git reset --hard origin/main
  else
    git pull --ff-only origin main
  fi
else
  echo "Cloning fresh project into: $PROJECT_DIR"
  if [ -e "$PROJECT_DIR" ]; then
    echo "Target path exists but is not a Git checkout: $PROJECT_DIR"
    echo "Move it manually before cloning to avoid deleting local files."
    exit 1
  fi
  git clone "$REPO_URL" "$PROJECT_DIR"
  cd "$PROJECT_DIR"
fi

echo
echo "Project ready. Starting Concrete Motivation AI..."
echo
python3 main.py
