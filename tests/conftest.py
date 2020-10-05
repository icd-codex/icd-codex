import pytest
from icdcodex import datacleaning


@pytest.fixture(scope="session")
def hierarchy_construction_intermediates():
    (H, _), untangle_elem, codes = datacleaning.build_icd10cm_hierarchy_from_zip(
        "tests/testdata/2020-ICD-10-CM-Codes.zip",
        "tests/testdata/2020-ICD-10-CM-Code-Tables.zip",
        return_intermediates=True
    )
    return H, untangle_elem, codes