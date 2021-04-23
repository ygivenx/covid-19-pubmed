# -*- coding: utf-8 -*-
import json
import os
import click
import logging
from pathlib import Path
from models import Base, Metadata
import pandas as pd

import dbconn

@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
def main(input_filepath):
    """ Load Metadata into postgres tables
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    # Create table if it doesn't exist
    load_data(input_filepath)


@dbconn.db_connection
def load_data(conn, input_filepath):
    """
    Load data from input file to postgres
    """
    Base.metadata.drop_all(conn.engine)
    Base.metadata.create_all(conn.engine)

    data = pd.read_csv(input_filepath, dtype={'sha': str,
                                                'pmcid': str,
                                                'pubmed_id': str,
                                                'doi': str,
                                                'Microsoft Academic Paper ID': str,
                                                'WHO #Covidence': str})

    data.columns =['cord_uid', 'sha', 'source_x', 'title', 'doi', 'pmcid', 'pubmed_id',
       'license', 'abstract', 'publish_time', 'authors', 'journal',
       'microsoft_academic_paper_id', 'who_covidence', 'has_pdf_parse',
       'has_pmc_xml_parse', 'full_text_file', 'url']

    data['paper_key'] = data.apply(lambda row: row.sha.strip() if row.sha is not None else row.pmcid.strip(), axis=1)
    data = data.drop_duplicates(subset=['paper_key'])
    data = data.to_json(orient='records')
    data = json.loads(data)
    for rec in data:
        rec['paper_key'] = rec['sha'] if rec['sha'] is not None else rec['pmcid']
        if rec['paper_key'] is not None:
            conn.session.add(Metadata(**rec))
    
                

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    

    main()
