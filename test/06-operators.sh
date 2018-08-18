#!/usr/bin/env bats

@test "count where total_energy > -15" {
  [ 12000 -eq $(abcd count where 'total_energy > -15') ]
}

@test "count where total_energy >= -15" {
  [ 12000 -eq $(abcd count where 'total_energy >= -15') ]
}

@test "count where total_energy < -15" {
  [ 47112 -eq $(abcd count where 'total_energy < -15') ]
}

@test "count where total_energy <= -15" {
  [ 47112 -eq $(abcd count where 'total_energy <= -15') ]
}
