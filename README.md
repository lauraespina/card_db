# ETL processes for CARD database

[![Python](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/) [![MySQL](https://img.shields.io/badge/MYSQL-blue)](https://www.mysql.com/)

Python scripts to automate ETL processes of getting coding sequences for antibiotic resistance genes into a relational database.

## Data sources

* CARD DATABASE: https://card.mcmaster.ca/ - Original info on the antibiotic resistance genes
* GENBANK DATABASE: https://www.ncbi.nlm.nih.gov/genbank/ - Source of the genomic sequences

## Libraries, frameworks and utilities

* SQLAlchemy: https://www.sqlalchemy.org/ - Toolkit and ORM for database access and updating.
* E-UTILITIES: https://www.ncbi.nlm.nih.gov/books/NBK25499/ - Utility to query DNA and Protein Accession codes to the Genbank database.
* Biopython: https://github.com/biopython/biopython - Toolkit for facilitating the parsing of genbank files.
* PANDAS: https://pandas.pydata.org/docs/index.html - Python library to work with dataframes.
* Others: [requests](https://pypi.org/project/requests/), [csv](https://pypi.org/project/python-csv/), [collections](https://docs.python.org/3/library/collections.html), [shutil](https://docs.python.org/3/library/shutil.html)

## Data destinations

* v1.0: Info stored in a relational database.
* v0.0: Worksheet for the final dataset, after txt files have been locally stored with the Genbank information.
