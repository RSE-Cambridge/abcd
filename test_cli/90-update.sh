#!/usr/bin/env bats

q='total_energy lt -269950'

@test "tag \"stuff=nice999\" where config_type = \"gamma_surface_112\"" {
  abcd tag \"stuff=nice999\" where config_type = \"gamma_surface_112\"
}

@test "tag \"scienceiscool\" where config_type = \"gamma_surface_110\"" {
  abcd tag \"scienceiscool\" where config_type = \"gamma_surface_110\"
}

