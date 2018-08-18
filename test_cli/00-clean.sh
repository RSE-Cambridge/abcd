#!/usr/bin/env bats

@test "delete (everything)" {
  abcd delete
}

@test "count == 0" {
  [ 0 -eq $(abcd count) ]
}
