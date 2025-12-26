#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAIRY_BIN="${FAIRY_BIN:-fairy}"

RULEPACK="${REPO_ROOT}/rulepacks/ena_webin_cli/rulepack.yaml"

OUT_DIR="${REPO_ROOT}/tests/golden/_actual"
mkdir -p "${OUT_DIR}"

run_one () {
  local label="$1"
  local fixture="$2"
  local expected="$3"

  local raw_json="${OUT_DIR}/report.${label}.raw.json"
  local norm_json="${OUT_DIR}/report.${label}.norm.json"

  "${FAIRY_BIN}" validate \
    --inputs default="${fixture}" \
    --rulepack "${RULEPACK}" \
    --report-json "${raw_json}"

  python3 "${REPO_ROOT}/scripts/normalize_report.py" "${raw_json}" "${norm_json}"

  if [[ ! -f "${expected}" || "${UPDATE_GOLDEN:-0}" == "1" ]]; then
    cp "${norm_json}" "${expected}"
    echo "✅ Golden updated: ${expected}"
  else
    diff -u "${expected}" "${norm_json}"
    echo "✅ Golden matches: ${expected}"
  fi
}

run_one "tsv" "${REPO_ROOT}/fixtures/tiny/annotations.tsv" "${REPO_ROOT}/tests/golden/expected_report.tsv.json"
run_one "csv" "${REPO_ROOT}/fixtures/tiny/annotations.csv" "${REPO_ROOT}/tests/golden/expected_report.csv.json"

echo "✅ All goldens passed"
