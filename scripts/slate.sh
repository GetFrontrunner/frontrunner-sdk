#!/usr/bin/env bash
set -ueo pipefail

# Do not use this in CI/CD; only use this locally. Requires docker.

REPO_ROOT="$(realpath "$(dirname "$0")/../")"

DOCS_DIR="${REPO_ROOT}/docs"
SLATE_OUTPUT_DIR="${REPO_ROOT}/dist/slate"

mkdir -p "${SLATE_OUTPUT_DIR}"

docker run \
  --rm \
  --publish 8000:4567 \
  --volume "${DOCS_DIR}:/srv/slate/source" \
  --volume "${SLATE_OUTPUT_DIR}:/srv/slate/build" \
  slatedocs/slate \
  "${1:-serve}" \
  ;
