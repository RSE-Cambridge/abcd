#!/usr/bin/env bats

q='total_energy lt -269950'

@test "update where interest=999 where config_type = \"gamma_surface_112\"" {
  abcd update science=\"iscool\" where config_type = \"gamma_surface_112\"
}

@test "update where science=\"iscool\" where config_type = \"gamma_surface_110\"" {
  abcd update science=\"iscool\" where config_type = \"gamma_surface_110\"
}

