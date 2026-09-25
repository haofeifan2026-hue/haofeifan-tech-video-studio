#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
codex_root="${CODEX_HOME:-$HOME/.codex}"
target_dir="$codex_root/skills/haofeifan-tech-video-studio"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      if [[ $# -lt 2 ]]; then
        echo "--target requires a directory" >&2
        exit 2
      fi
      target_dir="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: ./scripts/install.sh [--target DIRECTORY]"
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

python3 "$repo_root/scripts/validate_repo.py"

mkdir -p "$target_dir/agents" "$target_dir/references" "$target_dir/scripts"
cp "$repo_root/SKILL.md" "$target_dir/SKILL.md"
cp "$repo_root/agents/openai.yaml" "$target_dir/agents/openai.yaml"
cp -R "$repo_root/references/." "$target_dir/references/"
cp -R "$repo_root/scripts/." "$target_dir/scripts/"

echo "Installed haofeifan-tech-video-studio to $target_dir"
echo "Restart or refresh Codex to load the updated skill."
