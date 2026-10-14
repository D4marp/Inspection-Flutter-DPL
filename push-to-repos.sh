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
  local project_relative_path="flutter_projects/$folder"
  local temp_root
  local source_path
  local checkout_path
  local configured_remote
  local staged_files
  local file

  if [[ ! -f "$project_path/pubspec.yaml" ]]; then
    echo "ERROR: proyek tidak ditemukan: $project_path" >&2
    exit 1
  fi

  temp_root="$(mktemp -d "${TMPDIR:-/tmp}/dpl-push.XXXXXX")"
  source_path="$temp_root/source"
  checkout_path="$temp_root/repository"
  mkdir -p "$source_path"
  PUSH_TEMP_DIR="$temp_root"

  if ! git clone --quiet --branch main --single-branch "$remote_url" "$checkout_path"; then
    echo "ERROR: tidak dapat meng-clone branch main dari $remote_url" >&2
    exit 1
  fi

  git -C "$REPO_ROOT" archive --format=tar HEAD "$project_relative_path" |
    tar -xf - -C "$source_path" --strip-components=2

  while IFS= read -r file; do
    [[ -z "$file" ]] && continue
    if is_sensitive_file "$file"; then
      echo "ERROR: file berpotensi sensitif tidak akan di-push: $folder/$file" >&2
      exit 1
    fi
  done < <(find "$source_path" -type f -print)

  rsync -a --delete --exclude='/.git/' "$source_path/" "$checkout_path/"
  git -C "$checkout_path" add -A
  staged_files="$(git -C "$checkout_path" diff --cached --name-only)"

  while IFS= read -r file; do
    [[ -z "$file" ]] && continue
    if is_sensitive_file "$file"; then
      echo "ERROR: file berpotensi sensitif ter-stage dan push dibatalkan: $folder/$file" >&2
      exit 1
    fi
  done <<< "$staged_files"

  if ! git -C "$checkout_path" diff --cached --quiet; then
    local author_name="${GIT_AUTHOR_NAME:-$(git -C "$REPO_ROOT" config user.name || true)}"
    local author_email="${GIT_AUTHOR_EMAIL:-$(git -C "$REPO_ROOT" config user.email || true)}"
    if [[ -z "$author_name" || -z "$author_email" ]]; then
      echo "ERROR: identitas Git belum lengkap. Atur user.name dan user.email terlebih dahulu." >&2
      exit 1
    fi

    git -C "$checkout_path" -c user.name="$author_name" -c user.email="$author_email" \
      commit -m "$COMMIT_MSG"
  fi

  echo -e "${BLUE}Push $folder: $remote_url${NC}"
  git -C "$checkout_path" push -u origin main
  echo -e "${GREEN}Push $folder berhasil.${NC}"
  rm -rf -- "$temp_root"
  PUSH_TEMP_DIR=""
}

PUSH_TEMP_DIR=""
trap 'if [[ -n "$PUSH_TEMP_DIR" ]]; then rm -rf -- "$PUSH_TEMP_DIR"; fi' EXIT

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
