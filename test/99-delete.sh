#!/usr/bin/env bats

q='total_energy lt -269950'

@test "delete where $q" {
  [ 917 -eq $(abcd count where $q) ]
  abcd delete where $q
  [ 0 -eq $(abcd count where $q) ]
}

@test "delete (everything)" {
  abcd delete
  [ 0 -eq $(abcd count) ]
}
