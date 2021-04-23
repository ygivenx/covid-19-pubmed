# -*- coding: utf-8 -*-
import json
import os
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn external data from (../external) into
        text data ready to be processed (saved in ../raw).
    """
    logger = logging.getLogger(__name__)
    logger.info('get text data from jsons')

    for dirs in os.walk(input_filepath): # (external, [custom, bio] , [])
        for sub_dirs in dirs[1]:
            for ssdr in os.walk(dirs[0] + "/" + sub_dirs + "/" + sub_dirs):
                for fmtdir in ssdr[1]: 
                    for file_dir in os.walk(ssdr[0] + "/" + fmtdir):
                        for json_file in file_dir[2]:
                            with open(file_dir[0] + "/" +  json_file, "rb") as fp:
                                file_json = json.load(fp)

                            file_contents = dict()
                            body_list = list()
                            logger.info(sub_dirs[0]+ "/" +  json_file)

                            if "pdf_json" in input_filepath:

                                paper_id = file_json.get("paper_id")
                                abstracts = file_json.get("abstract")
                                title = file_json.get("title", "")
                                body = file_json.get("body_text")
                            else:
                                paper_id = file_json.get("paper_id")
                                abstracts = []
                                title = file_json["metadata"].get("title", "")
                                body = file_json.get("body_text")

                            logging.info("paperId: %s\nabstractLen: %s\ntitle: %s\nbodyLen: %d", paper_id, len(abstracts), title, len(body))

                            # Generate file content from json
                            file_contents["title"] = title
                            if len(abstracts) > 0:
                                file_contents["astract"] = abstracts[0].get("text")
                                logger.info("Abstract: %s", abstracts[0].get("text", ""))

                            for i in range(len(body)):
                                body_list.append(body[i].get("text", ""))
                            
                            file_contents["body"] = "\n\n".join(body_list)
                            logger.info("File Content length: %d", len(file_contents))
                            with open("data/raw/" + paper_id + ".json", 'w+') as wp:
                                json.dump(file_contents, wp)
                        

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
