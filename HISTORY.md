# History

## 0.4.3 (2020-10-04)
- Fix issue where hierarchy jsons were not being shipped with the pypi distribution

## 0.4.2 (2020-10-03)
- Add support for python <= 3.8 in the `hierarchy` module by using the `importlib.resources` backport

## 0.4.1 (2020-09-11)
- Update PyPI metadata

## 0.4.0 (2020-09-11)
- ICD-10-CM (2019 to 2020) codes are now fully present (whereas hackathon version missed certain codes)
- Versions of the ICD 9 and ICD-10-CM hierarchies are now cached to the `data` module
- Changed the hierarchy API: `hierarchy.icd9hierarchy()` is now `hierarchy.icd9()`. Ditto for ICD-10-CM.

## 0.3.0 (2020-09-05)
- Finesse API, now consistent between documentation and implementation

## 0.1.0 (2020-09-04)
- First release on PyPI, testing the waters during hackathon
