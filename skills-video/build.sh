#!/usr/bin/env bash
# Renders skills-video/index.html to out/15-free-claude-skills-9x16.mp4
#
#   ./build.sh              # 1080x1920 @ 30fps, ~30s
#   ./build.sh --fps 60     # smoother, ~2x the frames
#
# Requires: node + playwright (chromium) and ffmpeg with libx264 on PATH.
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -e node_modules ]; then
  if [ -d /opt/node22/lib/node_modules/playwright ]; then
    ln -sfn /opt/node22/lib/node_modules node_modules
  else
    npm install playwright
  fi
fi

command -v ffmpeg >/dev/null || {
  echo "ffmpeg not found; install it, or: pip install imageio-ffmpeg and link the bundled binary" >&2
  exit 1
}

node render.mjs "$@"
