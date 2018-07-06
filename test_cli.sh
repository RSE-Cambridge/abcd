#!/bin/bash
set -euo pipefail

dir=$(dirname $0)
q="total_energy gt -15"

function run_abcd {
  echo "$ abcd $@"
  python abcd.py $@
  echo
}

run_abcd import data/*.xyz

run_abcd count
run_abcd count where $q
run_abcd keys
run_abcd keys where $q
run_abcd stats total_energy
run_abcd stats total_energy where $q
run_abcd stats total_energy degauss
run_abcd stats total_energy degauss where $q
run_abcd delete where total_energy lt -269950
