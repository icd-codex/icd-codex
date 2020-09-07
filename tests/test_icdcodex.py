#!/usr/bin/env python

"""Tests for `icdcodex` package."""

import pytest
from icdcodex import hierarchy as h, icd2vec as iv, datacleaning as cleaning

def test_encode_decode_icd9():
    G, _ = h.icd9hierarchy()
    G_orig, _ = cleaning.build_icd9_hierarchy("nbexamples/icd9Hierarchy.json")
    assert set(G.nodes()) == set(G_orig.nodes())

def test_encode_decode_icd10():
    raise NotImplementedError