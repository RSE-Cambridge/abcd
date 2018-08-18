#!/usr/bin/env bats

q='total_energy lt -269950'

@test "update stuff 999 where config_type = \"gamma_surface_112\"" {
  n=$(abcd count where config_type = \"gamma_surface_112\")
  abcd tag stuff 999 where config_type = \"gamma_surface_112\"
  [ $n -eq $(abcd count where stuff = 999) ]
}

@test "update tag \"scienceiscool\" where config_type = \"gamma_surface_110\"" {
  n=$(abcd count where config_type = \"gamma_surface_110\")
  abcd tag tag \"scienceiscool\" where config_type = \"gamma_surface_110\"
  [ $n -eq $(abcd count where tag = \"scienceiscool\") ]
}

