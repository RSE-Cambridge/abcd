#!/usr/bin/env bats

q='total_energy lt -269950'

@test "delete where $q" {
n_before=$(abcd count where $q)
abcd delete where $q
n_after=$(abcd count where $q)
[ 917 -eq $n_before  -a 0 -eq $n_after ]
}
