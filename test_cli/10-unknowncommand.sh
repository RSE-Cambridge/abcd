#!/usr/bin/env bats

@test "notacmd -> error" {
  ! abcd notacmd
}
