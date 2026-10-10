#!/usr/bin/env bash
# One-time setup: pinned Premiere MCP connector + WhisperX venv.
# Run by David (disk-hold exception approved 2026-10-10); the disk-floor hook blocks agents from running it.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CONNECTOR_DIR="$REPO_ROOT/vendor/premiere-mcp"
CONNECTOR_URL="https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP.git"
CONNECTOR_COMMIT="12684e37297a702265985dffa7d33629d28074f4" # tag v1.2.3
WHISPERX_VENV="$HOME/.cache/video-editor/whisperx-venv"

echo "== Premiere MCP connector (v1.2.3)"
if [ ! -d "$CONNECTOR_DIR/.git" ]; then
  git clone --quiet "$CONNECTOR_URL" "$CONNECTOR_DIR"
fi
git -C "$CONNECTOR_DIR" checkout --quiet "$CONNECTOR_COMMIT"
[ "$(git -C "$CONNECTOR_DIR" rev-parse HEAD)" = "$CONNECTOR_COMMIT" ] || { echo "connector not at pinned commit" >&2; exit 1; }
# Lockfile install without dependency lifecycle scripts, then compile.
(cd "$CONNECTOR_DIR" && npm ci --ignore-scripts --no-audit --no-fund && npm run build)
[ -f "$CONNECTOR_DIR/dist/cli.js" ] || { echo "connector build missing dist/cli.js" >&2; exit 1; }

echo "== WhisperX venv"
if [ ! -x "$WHISPERX_VENV/bin/python" ]; then
  mkdir -p "$(dirname "$WHISPERX_VENV")"
  uv venv --python 3.11 "$WHISPERX_VENV"
fi
uv pip install --python "$WHISPERX_VENV/bin/python" whisperx
"$WHISPERX_VENV/bin/python" -c "import whisperx; print('whisperx ok')"

echo "== Done. Disk free now:"
df -h / | tail -1
