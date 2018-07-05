#!/usr/bin/env python

from pytest import fixture

@fixture
def db():
    import abcd
    return abcd.ABCD('postgresql://localhost')

def test_count(db):
    db.count()

def test_select(db):
    db.select('total_energy')

def test_keys(db):
    db.keys()
