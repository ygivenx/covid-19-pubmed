from elasticsearch import Elasticsearch
import glob
import json
import dbconn
from models import Metadata

@dbconn.db_connection
def get_metadata(conn, paper_key):
    print(paper_key)
    res = conn.session.query(Metadata.paper_key).filter(Metadata.paper_key == paper_key).scalar()
    print(res)


es = Elasticsearch([{'host':'localhost', 'port': 9200}])

for i, paper in enumerate(glob. glob("data/raw/*")):
    with open(paper) as fp:
        meta = get_metadata(paper.rsplit("/")[-1].split(".")[0])
        print(meta)
        # es.index(index="covid", doc_type='paper', id=i, body=json.load(fp))
