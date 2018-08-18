#!/usr/bin/env bats

@test "keys" {
diff <(abcd keys) - <<EOF
count           key key_type
14143   config_name   string
59112   config_type   string
14143       degauss   number
14143       ecutwfc   number
59112        energy   number
14143       kpoints    array
  332     timestamp   number
59112  total_energy   number
24002        virial    array
  549    virial_not    array
EOF
}

@test "keys where total_energy gt -15" {
diff <(abcd keys where total_energy gt -15) - <<EOF
count           key key_type
12000   config_type   string
12000        energy   number
12000  total_energy   number
12000        virial    array
EOF
}
