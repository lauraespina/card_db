# ETL processes for CARD database

[![Python](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)

Python scripts to automate ETL processes of getting coding sequences for antibiotic resistance genes into worksheets and SQL databases.

## Data sources

* CARD DATABASE: https://card.mcmaster.ca/ - Original info on the antibiotic resistance genes
* GENBANK DATABASE: https://www.ncbi.nlm.nih.gov/genbank/ - Source of the genomic sequences

## Libraries, frameworks and utilities

* E-UTILITIES: https://www.ncbi.nlm.nih.gov/books/NBK25499/ - Utility to query DNA and Protein Accession codes to the Genbank database.
* Biopython: https://github.com/biopython/biopython - Toolkit for facilitating the parsing of genbank files.
* PANDAS: https://pandas.pydata.org/docs/index.html - Python library to work with dataframes.
* Others: [requests](https://pypi.org/project/requests/), [csv](https://pypi.org/project/python-csv/), [collections](https://docs.python.org/3/library/collections.html), [shutil](https://docs.python.org/3/library/shutil.html)

## Data destinations

* v0.0: Worksheet for the final dataset.
