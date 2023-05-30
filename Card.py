"""Definition of the Card class containing all the genomic info for each object
"""

import pandas as pd
from Bio.Seq import Seq

class Card:

    def __init__(self):
        self.DNA_Accession = ''
        self.Protein_Accession = ''
        self.DNA_Sequence = ''
        self.DNA_CDS = ''
        self.prot_CDS = ''
        self.delimiter = ''
        self.CDS_seq = ''
        self.additional_info = ''

    def update_delimiters(self):
        if str(self.DNA_CDS) != '':
            self.delimiter = str(self.DNA_CDS).split(':')
            for i in range(2):
                self.delimiter[i] = int(''.join(c for c in self.delimiter[i] if c.isdigit()))
                self.additional_info = 'Seq from DNA_Accession info, CDS(+)'
            if self.DNA_CDS.endswith('(-)'):
                self.delimiter = [len(str(self.DNA_Sequence)) - element for element in self.delimiter]
                self.delimiter = list(reversed(self.delimiter))
                self.additional_info = 'Seq from DNA_Accession info, CDS(-)'
        if str(self.DNA_CDS) == '' and str(self.prot_CDS) != '':
            self.delimiter = (str(self.prot_CDS)).split(':')[1]
            self.delimiter = self.delimiter.split('..')
            self.delimiter[0] = int(''.join(c for c in self.delimiter[0] if c.isdigit())) - 1
            self.delimiter[1] = int(''.join(c for c in self.delimiter[1] if c.isdigit()))
            self.additional_info = 'Seq from Protein_Accession info, CDS(+)'
            if self.prot_CDS.startswith('complement'):
                self.delimiter = [len(str(self.DNA_Sequence)) - element for element in self.delimiter]
                self.delimiter = list(reversed(self.delimiter))
                self.additional_info = 'Seq from Protein_Accession info, CDS(-)'
        if str(self.DNA_CDS) == '' and str(self.prot_CDS) == '':
            self.delimiter = [0, len(str(self.DNA_Sequence))]
            self.additional_info = 'Whole DNA_Sequence'

    def define_sequence(self):
        if self.additional_info.endswith('(+)'):
            self.CDS_seq = Seq(self.DNA_Sequence)[self.delimiter[0]:self.delimiter[1]]
        elif self.additional_info.endswith('(-)'):
            self.CDS_seq = Seq(self.DNA_Sequence).reverse_complement()[self.delimiter[0]:self.delimiter[1]]