[![PyPI version fury.io](https://badge.fury.io/py/icdcodex.svg)](https://pypi.python.org/pypi/icdcodex/) [![Documentation Status](https://readthedocs.org/projects/icd-codex/badge/?version=latest)](http://icd-codex.readthedocs.io/?badge=latest) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![GitHub license](https://img.shields.io/github/license/icd-codex/icd-codex.svg)](https://github.com/icd-codex/icd-codex/blob/master/LICENSE)

```{admonition} Experimental 
This is experimental software and a stable API is not expected until version 1.0
```
## What is it?
A python library for providing vector representation of ICD-9 and ICD-10 codes. Because it takes advantage of the hierarchical nature of ICD codes, it also provides these hierarchies in a [`networkx`](https://networkx.github.io) format.

## Motivation
`icdcodex` was the first prize winner in the Data Driven Healthcare Track of John Hopkins' [MedHacks 2020](https://medhacks2020.devpost.com). It was hacked together to address the problem of [ICD](https://en.wikipedia.org/wiki/ICD-10) miscodes, which is a major issue for health insurance in the United States. Indeed, while ICD coding is tedious and labour intensive, it is not obvious how to automate because the output space is enourmous. For example, ICD-10 CM (clinical modification) has over 70,000 codes and growing.

There are [many strategies](https://maxhalford.github.io/blog/target-encoding/) for target encoding that address these issues. `icdcodex` has two features that make ICD classification more amenable to modeling:
- Access to a `networkx` tree representation of the ICD-9 and ICD-10 hierarchies
- Vector embeddings of ICD codes using the [node2vec](https://arxiv.org/abs/1607.00653) algorithm (including pre-computed embeddings and an interface to create new embeddings)

## Example Code
```python
from icdcodex import icd2vec, hierarchy
embedder = icd2vec.Icd2Vec(num_embedding_dimensions=64)
embedder.fit(*hierarchy.icd9())
X = get_patient_covariates()
y = embedder.to_vec(["001.0"])  # Cholera due to vibrio cholerae
```
In this case, `y` is a 64-dimensional vector close to other `Infectious And Parasitic Diseases` codes. 

## Related Work
- node2vec [Paper](https://cs.stanford.edu/people/jure/pubs/node2vec-kdd16.pdf), [Website](https://snap.stanford.edu/node2vec/), [Code](https://github.com/snap-stanford/snap/tree/master/examples/node2vec), [Alternate Code](https://github.com/eliorc/node2vec)
- Learning Low-Dimensional Representations of Medical Concepts: [Paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5001761/), [Code](https://github.com/clinicalml/embeddings)

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
