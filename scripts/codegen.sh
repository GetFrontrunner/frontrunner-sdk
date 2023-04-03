#!/usr/bin/env bash
set -ueo pipefail

REPO_ROOT="$(realpath "$(dirname "$0")/../")"

APIS="$(
  find openapi -name openapi.json \
  | xargs dirname \
  | sed -e 's/openapi\///' \
)"

function check_required_command() {
  if ! type "${1}"; then
    echo "Missing command: ${1}"
    echo
    echo "  brew install ${1}"
    echo
    exit 1
  fi
}

check_required_command swagger-codegen
check_required_command pants

function to_python_package_name() {
  package_name="$1"
  package_name="${package_name//[-]/_}"
  package_name="${package_name//[\/]/.}"
  package_name="frontrunner_sdk.openapi.${package_name}"
  package_name="$(echo "${package_name}" | tr -s '_.')"
  echo "${package_name}"
}

for api in ${APIS[@]}; do
  rm -rf "${REPO_ROOT}/dist/codegen/${api}"

  package_name="$(to_python_package_name "${api}")"
  package_dir="${package_name//[.]//}"

  swagger-codegen generate \
    --input-spec "${REPO_ROOT}/openapi/${api}/openapi.json" \
    --output "${REPO_ROOT}/dist/codegen/${api}" \
    --lang python \
    --library asyncio \
    -DpackageName="${package_name}" \
    ;

  cp \
    "${REPO_ROOT}/dist/codegen/${api}/requirements.txt" \
    "${REPO_ROOT}/openapi/${api}/requirements.txt" \
    ;

  mkdir -p "${REPO_ROOT}/${package_dir}/"

  rsync \
    --recursive \
    --force \
    --delete-after \
    "${REPO_ROOT}/dist/codegen/${api}/${package_dir}/" \
    "${REPO_ROOT}/${package_dir}/" \
    ;
done

pants tailor ::
pants export ::
