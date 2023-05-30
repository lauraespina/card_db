import sqlalchemy
import FactoryDb
from sqlalchemy import update

class UpdateDb():
    def create_column(table, column, column_type):
        query = f'ALTER TABLE {table} ADD {column} {column_type} ;'
        return FactoryDb.engine.connect().execute(query)

    def update_column(tablename, dictionary, column):
        md = sqlalchemy.MetaData(bind=FactoryDb.engine)
        table = sqlalchemy.Table(tablename, md, autoload=True)
        if column == 'CDS_Sequence':
            column_expression = table.c.CDS_Sequence
        if column == 'Extra_info':
            column_expression = table.c.Extra_info
        for k, v in dictionary.items():
            upd = update(table).where(table.c.ARO_Accession == k).values({column_expression: v})
            FactoryDb.engine.execute(upd)