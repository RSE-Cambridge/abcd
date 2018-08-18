#!/usr/bin/env bats

@test "notacmd -> error" {
  ! abcd notacmd
}

@test "count where bla blah" {
  ! abcd where bla blah
}
