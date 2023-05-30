"""Definition of the classes that will be mapped to the database
"""

from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import LONGBLOB

import Connection

# Connection details and metadata creation
engine, session, Base = Connection.CreateConnection()

class AROs(Base):
    __tablename__ = 'card_fact_table'
    ARO_Accession = Column(String(255), primary_key = True)
    CVTERM_ID = Column(String(255))
    Model_Sequence_ID = Column(String(255))
    Model_ID = Column(String(255))
    Model_Name = Column(String(255))
    ARO_Name = Column(String(255))
    Protein_Accession = Column(String(255))
    DNA_Accession = Column(String(255))
    AMR_Gene_Family = Column(String(255))
    Drug_Class = Column(String(400))
    Resistance_Mechanism = Column(String(255))
    CARD_Short_Name = Column(String(255))

    @classmethod
    def get_unique(cls, ARO_Accession, CVTERM_ID, Model_Sequence_ID, Model_ID, Model_Name, ARO_Name, Protein_Accession,
                 DNA_Accession, AMR_Gene_Family, Drug_Class, Resistance_Mechanism, CARD_Short_Name):
        """Method to parse non-duplicated ARO objects into the card fact table."""
        cache = session._unique_cache = getattr(session, '_unique_cache', {})
        key = (cls, ARO_Accession)
        o = cache.get(key)
        if o is None:
            o = session.query(cls).filter_by(ARO_Accession=ARO_Accession).first()
            if o is None:
                o = cls(ARO_Accession = ARO_Accession, CVTERM_ID = CVTERM_ID, Model_Sequence_ID = Model_Sequence_ID, Model_ID = Model_ID, Model_Name = Model_Name, ARO_Name = ARO_Name, Protein_Accession = Protein_Accession,
                 DNA_Accession = DNA_Accession, AMR_Gene_Family = AMR_Gene_Family, Drug_Class = Drug_Class, Resistance_Mechanism = Resistance_Mechanism, CARD_Short_Name = CARD_Short_Name)
                session.add(o)
            cache[key] = o
        return o


class FASTA(Base):
    __tablename__ = 'fasta_table'
    DNA_Accession = Column(String(255), primary_key = True)
    DNA_Sequence = Column(LONGBLOB)
    description = Column(String(1255))


    def __init__(self, DNA_Accession, DNA_Sequence, description):
        self.DNA_Accession = DNA_Accession
        self.DNA_Sequence = DNA_Sequence
        self.description = description

    @classmethod
    def get_unique(cls, DNA_Accession, DNA_Sequence, description):
        """Method to parse non-duplicated FASTA objects into the fasta table."""
        cache = session._unique_cache = getattr(session, '_unique_cache', {})
        key = (cls, DNA_Accession)
        o = cache.get(key)
        if o is None:
            o = session.query(cls).filter_by(DNA_Accession=DNA_Accession).first()
            if o is None:
                o = cls(DNA_Accession=DNA_Accession, DNA_Sequence=DNA_Sequence, description=description)
                session.add(o)
            cache[key] = o
        return o


class CDS(Base):
    __tablename__ = 'cds_table'
    ARO_Accession = Column(String(255), primary_key = True)
    DNA_Accession = Column(String(255))
    Protein_Accession = Column(String(255))
    Location_DNA = Column(String(255))
    Location_Prot = Column(String(255))

    @classmethod
    def get_unique(cls, ARO_Accession, DNA_Accession, Protein_Accession, Location_DNA, Location_Prot):
        cache = session._unique_cache = getattr(session, '_unique_cache', {})
        key = (cls, ARO_Accession)
        o = cache.get(key)
        if o is None:
            o = session.query(cls).filter_by(ARO_Accession=ARO_Accession).first()
            if o is None:
                o = cls(ARO_Accession=ARO_Accession, DNA_Accession = DNA_Accession, Protein_Accession = Protein_Accession,
                        Location_DNA=Location_DNA, Location_Prot=Location_Prot)
                session.add(o)
            cache[key] = o
        return o

class Delimiters(Base):
    __tablename__ = 'delimiters_table'
    ARO_Accession = Column(String(255), primary_key=True)
    DNA_Accession = Column(String(255))
    Strand = Column(String(1))
    Delimiter_initial = Column(String(255))
    Delimiter_final = Column(String(255))
    Extra_info = Column(String(255))

    def __init__(self, ARO_Accession, DNA_Accession, Strand, Delimiter_initial, Delimiter_final, Extra_info):
        self.ARO_Accession = ARO_Accession
        self.DNA_Accession = DNA_Accession
        self.Strand = Strand
        self.Delimiter_initial = Delimiter_initial
        self.Delimiter_final = Delimiter_final
        self.Extra_info = Extra_info

Base.metadata.create_all(bind= engine)
