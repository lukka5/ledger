======
ledger
======


.. image:: https://img.shields.io/pypi/v/ledger.svg
        :target: https://pypi.python.org/pypi/ledger

.. image:: https://img.shields.io/travis/lukka5/ledger.svg
        :target: https://travis-ci.com/lukka5/ledger

.. image:: https://readthedocs.org/projects/ledger/badge/?version=latest
        :target: https://ledger.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/lukka5/ledger/shield.svg
     :target: https://pyup.io/repos/github/lukka5/ledger/
     :alt: Updates



Ledger - Keep track of financial transactions between different parties, people and organisations.


* Free software: MIT license
* Documentation: https://ledger.readthedocs.io.


Features
--------

* Load transaction in CSV format
* Calculate the balance for an entity at any given date


Install
-------

To install it first clone this repo and then::

    pip setup.py install

Run tests with::

    pytest


Usage
-----

Given a sample CSV file ``expenses.csv`` with the following transactions:

.. code-block:: shell

    2015-01-16,john,mary,125.00
    2015-01-17,john,supermarket,20.00
    2015-01-17,mary,insurance,100.00

We can load it and calculate the balance for a entity at a given date:

.. code-block:: python

    from datetime import date

    from ledger import Ledger

    ledger = Ledger()
    ledger.load_from_file('expenses.csv')
    balance = ledger.get_balance('mary', date(2015, 1, 17))
    balance.amount  # Decimal('25.00')


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
