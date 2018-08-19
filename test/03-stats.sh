#!/usr/bin/env bats

@test "stats total_energy" {
diff <(abcd stats total_energy) - <<EOF
        total_energy
count   59112.000000
mean   -18677.444930
std     60558.715973
min   -449910.248128
25%     -3460.893854
50%      -132.677221
75%      -126.756328
max       -10.822042
EOF
}

@test "stats total_energy where total_energy gt -15" {
diff <(abcd stats total_energy where total_energy gt -15) - <<EOF
       total_energy
count  12000.000000
mean     -11.099061
std        0.063193
min      -11.194835
25%      -11.143843
50%      -11.109441
75%      -11.065003
max      -10.822042
EOF
}

@test "stats total_energy ecutwfc" {
diff <(abcd stats total_energy ecutwfc) - <<EOF
            ecutwfc   total_energy
count  1.414300e+04   59112.000000
mean   1.224512e+03  -18677.444930
std    2.273817e-13   60558.715973
min    1.224512e+03 -449910.248128
25%    1.224512e+03   -3460.893854
50%    1.224512e+03    -132.677221
75%    1.224512e+03    -126.756328
max    1.224512e+03     -10.822042
EOF
}

@test "stats total_energy ecutwfc where total_energy gt -15" {
diff <(abcd stats total_energy ecutwfc where total_energy gt -15) - <<EOF
       total_energy
count  12000.000000
mean     -11.099061
std        0.063193
min      -11.194835
25%      -11.143843
50%      -11.109441
75%      -11.065003
max      -10.822042
EOF
}
