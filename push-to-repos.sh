#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECTS_ROOT="$REPO_ROOT/flutter_projects"

MAIN_REMOTE="https://github.com/D4marp/Inspection-Flutter-DPL.git"
DAY_2_REMOTE="https://github.com/D4marp/Inspection-Flutter-DPL-2.git"
DAY_3_REMOTE="https://github.com/D4marp/Inspection-Flutter-DPL-3.git"
COMMIT_MSG="${COMMIT_MSG:-chore: sync Flutter training project}"
TARGET="${1:-all}"

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

usage() {
  echo "Usage: $0 [all|main|day2|day3]"
}

is_sensitive_file() {
  local file="$1"
  local base
  base="$(basename -- "$file")"

  case "$base" in
    .env.example|.env.sample|.env.template)
      return 1
      ;;
    .env|.env.*|key.properties|*.jks|*.keystore|*.p12|*.mobileprovision|*.pem|*.key)
      return 0
      ;;
  esac

  return 1
}

assert_clean_root() {
  if [[ -n "$(git -C "$REPO_ROOT" status --porcelain)" ]]; then
    echo "ERROR: repo utama punya perubahan lokal yang belum di-commit." >&2
    echo "Commit atau simpan perubahan sebelum menjalankan push." >&2
    git -C "$REPO_ROOT" status --short >&2
    exit 1
  fi
}

push_main_repository() {
  local configured_remote
  configured_remote="$(git -C "$REPO_ROOT" remote get-url origin)"
  if [[ "$configured_remote" != "$MAIN_REMOTE" ]]; then
    echo "ERROR: origin repo utama tidak sesuai." >&2
    echo "  Diharapkan: $MAIN_REMOTE" >&2
    echo "  Saat ini:   $configured_remote" >&2
    exit 1
  fi

  echo -e "${BLUE}Push repo utama: $MAIN_REMOTE${NC}"
  git -C "$REPO_ROOT" push -u origin HEAD:main
  echo -e "${GREEN}Push repo utama berhasil.${NC}"
}

push_project() {
  local folder="$1"
  local remote_url="$2"
  local project_path="$PROJECTS_ROOT/$folder"
  local configured_remote
  local staged_files
  local file

  if [[ ! -f "$project_path/pubspec.yaml" ]]; then
    echo "ERROR: proyek tidak ditemukan: $project_path" >&2
    exit 1
  fi

  if [[ "$(git -C "$project_path" rev-parse --show-toplevel 2>/dev/null || true)" != "$project_path" ]]; then
    git -C "$project_path" init -b main
  fi

  if git -C "$project_path" remote get-url origin >/dev/null 2>&1; then
    configured_remote="$(git -C "$project_path" remote get-url origin)"
    if [[ "$configured_remote" != "$remote_url" ]]; then
      echo "ERROR: origin di $folder mengarah ke remote berbeda: $configured_remote" >&2
      exit 1
    fi
  else
    git -C "$project_path" remote add origin "$remote_url"
  fi

  if [[ -n "$(git -C "$project_path" diff --cached --name-only)" ]]; then
    echo "ERROR: $folder sudah memiliki perubahan yang di-stage. Periksa dulu sebelum push." >&2
    exit 1
  fi

  local author_name="${GIT_AUTHOR_NAME:-$(git -C "$REPO_ROOT" config user.name || true)}"
  local author_email="${GIT_AUTHOR_EMAIL:-$(git -C "$REPO_ROOT" config user.email || true)}"
  if [[ -z "$author_name" || -z "$author_email" ]]; then
    echo "ERROR: identitas Git belum lengkap. Atur user.name dan user.email terlebih dahulu." >&2
    exit 1
  fi

  git -C "$project_path" add -A
  staged_files="$(git -C "$project_path" diff --cached --name-only)"
  while IFS= read -r file; do
    [[ -z "$file" ]] && continue
    if is_sensitive_file "$file"; then
      echo "ERROR: file berpotensi sensitif tidak akan di-push: $folder/$file" >&2
      exit 1
    fi
  done <<< "$staged_files"

  if ! git -C "$project_path" diff --cached --quiet; then
    git -C "$project_path" -c user.name="$author_name" -c user.email="$author_email" \
      commit -m "$COMMIT_MSG"
  fi

  git -C "$project_path" branch -M main

  echo -e "${BLUE}Push $folder: $remote_url${NC}"
  git -C "$project_path" push -u origin main
  echo -e "${GREEN}Push $folder berhasil.${NC}"
}

case "$TARGET" in
  all|main|day2|day3) ;;
  *)
    usage >&2
    exit 2
    ;;
esac

"$REPO_ROOT/pre-push-check.sh"
assert_clean_root

case "$TARGET" in
  all)
    push_main_repository
    push_project "hari_2_dpl_inspection_api" "$DAY_2_REMOTE"
    push_project "hari_3_dpl_inspection_release" "$DAY_3_REMOTE"
    ;;
  main)
    push_main_repository
    ;;
  day2)
    push_project "hari_2_dpl_inspection_api" "$DAY_2_REMOTE"
    ;;
  day3)
    push_project "hari_3_dpl_inspection_release" "$DAY_3_REMOTE"
    ;;
esac

echo -e "${GREEN}Semua target yang dipilih selesai di-push.${NC}"
