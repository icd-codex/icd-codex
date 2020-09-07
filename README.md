[![PyPI version fury.io](https://badge.fury.io/py/icdcodex.svg)](https://pypi.python.org/pypi/icdcodex/) [![Documentation Status](https://readthedocs.org/projects/icd-codex/badge/?version=latest)](http://icd-codex.readthedocs.io/?badge=latest) [![GitHub license](https://img.shields.io/github/license/icd-codex/icd-codex.svg)](https://github.com/icd-codex/icd-codex/blob/master/LICENSE)


`icdcodex` was the first prize winner in the Data Driven Healthcare Track of John Hopkins' [MedHacks 2020](https://medhacks2020.devpost.com).

## Motivation

> The International Classification of Diseases, Clinical Modification is used to code and classify morbidity data from the inpatient and outpatient records, physician offices, and most National Center for Health Statistics (NCHS) surveys.
> [https://www.cdc.gov/nchs/icd/index.htm](https://www.cdc.gov/nchs/icd/index.htm)

Thousands of Americans are wrongly misquoted on their health insurance yearly due to ICD miscodes. While ICD coding is tedious and labour-intensive, it is difficult to automate by machine learning because the output space is enormous. For example, ICD-10 CM (clinical modification) has over 70,000 codes and growing. `icdcodex` has two features that make ICD classification more amenable to modeling.
- Access to a networkx tree representation of the ICD9 and ICD10 hierarchies
- Vector embeddings of ICD codes (including pre-computed embeddings and an interface to create new embeddings)

## Example Usage

```python
from icdcodex import icd2vec, hierarchy
embedder = icd2vec.Icd2Vec(num_embedding_dimensions=64)
embedder.fit(*hierarchy.icd9hierarchy())
X = get_patient_covariates()
y = embedder.to_vec(["A00.0"])  # Cholera due to vibrio cholerae
```
In this case, `y` is a 64-dimensional vector close to other `Infectious And Parasitic Diseases` codes. 

## The Hackathon Team
- Jeremy Fisher (Maintainer)
- Alhusain Abdalla
- Natasha Nehra
- Tejas Patel
- Hamrish Saravanakumar

## Documentation

See the full documentation: [https://icd-codex.readthedocs.io/en/latest/](https://icd-codex.readthedocs.io/en/latest/)

## Contributions

[Contributions are always welcome!](https://icd-codex.readthedocs.io/en/latest/contributing.html)
