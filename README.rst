========
icdcodex
========

.. image:: https://img.shields.io/pypi/v/icdcodex.svg
        :target: https://pypi.python.org/pypi/icdcodex


.. image:: https://readthedocs.org/projects/icdcodex/badge/?version=latest
        :target: https://icdcodex.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

ICD embedding for machine learning, created for `MedHacks2020 ❤️
<http://medhacks.org/?fbclid=IwAR0L-JQotA_wdVe5PTySOrPMCCknlZBb8xlHmwCkcyWPEFwTeVlk3jkyuJg/>`_.

* Free software: MIT license
* Documentation: https://icdcodex.readthedocs.io.

What is Medhacks?
-----------------
MedHacks hosted by Johns Hopkins University aims to unite talented and diverse minds from all backgrounds in order to foster a collaborative environment that aims to solve the world’s medical obstacles and issues. 

The Problem
-----------
ICD coding is a laborous, but difficult to automate by machine learning because the output space if intractably large. (ICD-10CM has over 70,000 codes.) icdcodex creates a vector embedding for this input space, making it simpler for machine learning practioners to efficiently adapt algorithms for ICD coding.

Our Solution
------------
We rely on the word2vec model to generate this embedding. In this set up, each ICD code represents a "word," whereas a path sampled from breadth-first or depth-first search represents the "sentence."


The Team
--------
* Jeremy Adams Fisher
* Alhusain Abdalla
* Natasha Nehra
* Tejas Patel
* Hamrish Saravanakumar


Features
--------

* Curated networkX graphs representing ICD hierarchies
* A simple API to generate 

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
