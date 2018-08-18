#!/usr/bin/env bats

@test "read data/*.xyz" {
  abcd read data/*.xyz
}

@test "count == 59112" {
  [ 59112 -eq $(abcd count) ]
}

@test "count where total_energy gt -15" {
  [ 12000 -eq $(abcd count where total_energy gt -15) ]
}
