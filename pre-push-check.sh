#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

projects=(
  "flutter_projects/hari_1_dpl_inspection"
  "flutter_projects/hari_2_dpl_inspection_api"
  "flutter_projects/hari_3_dpl_inspection_release"
)

for project in "${projects[@]}"; do
  project_path="$REPO_ROOT/$project"
  if [[ ! -f "$project_path/pubspec.yaml" ]]; then
    echo "ERROR: pubspec.yaml tidak ditemukan di $project_path" >&2
    exit 1
  fi
done

expected_remote="https://github.com/D4marp/Inspection-Flutter-DPL.git"
configured_remote="$(git -C "$REPO_ROOT" remote get-url origin)"
if [[ "$configured_remote" != "$expected_remote" ]]; then
  echo "ERROR: origin repo utama tidak sesuai: $configured_remote" >&2
  exit 1
fi

echo "Pre-push check lulus: repo utama dan tiga proyek Flutter ditemukan."
