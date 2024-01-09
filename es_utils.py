from elasticsearch import Elasticsearch
from . import es_config

def create_index_if_not_exists(index_name):
    es = Elasticsearch()
    if not es.indices.exists(index_name):
        es.indices.create(index=index_name, body=es_config.INDEX_SETTINGS)
