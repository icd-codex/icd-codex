import pytest
from icdcodex import hierarchy


@pytest.mark.smoke
def test_icd9():
    hierarchy.icd9()


@pytest.mark.smoke
@pytest.mark.parametrize("version", [None, "2019", "2020", "2021"])
def test_icd10cm(version):
    hierarchy.icd10cm(version=version)


@pytest.mark.parametrize("hierarchy, codes", [
    hierarchy.icd9(),
    hierarchy.icd10cm("2019"),
    hierarchy.icd10cm("2020"),
    hierarchy.icd10cm("2021")
])
def test_ensure_all_codes_present(hierarchy, codes):
    for code in codes:
        assert code in hierarchy.nodes()
