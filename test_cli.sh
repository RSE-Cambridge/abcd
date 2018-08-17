#!/bin/bash
set -euo pipefail

q="total_energy gt -15"

set -x
abcd read data/*.xyz

abcd count
abcd count where $q
abcd keys
abcd keys where $q
abcd stats total_energy
abcd stats total_energy where $q
abcd stats total_energy degauss
abcd stats total_energy degauss where $q

abcd hist config_type
abcd count where config_type = \"bcc_bulk_54_high\"

q='total_energy lt -269950'
abcd count  where $q
abcd delete where $q
abcd count  where $q
