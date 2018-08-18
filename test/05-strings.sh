#!/usr/bin/env bats

@test "count where config_type = \"bcc_bulk_54_high\"" {
[ 28 -eq $(abcd count where config_type = \"bcc_bulk_54_high\") ]
}
