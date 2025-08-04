from typing import List, Tuple, Union, Dict
import json
from tqdm import tqdm
from elasticsearch import Elasticsearch
from config import config

def build_elasticsearch(index_name, file_path):
    es = Elasticsearch([f'http://localhost:{config["port"]}'],)

    # 定义索引名和索引设置
    index_body = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "content": {"type": "text", "similarity": "BM25"
                },
                "id": {"type": "integer"}
            }
        }
    }

    # create index
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body=index_body)
        print(f"Index '{index_name}' created successfully.")
    else:
        print(f"Index '{index_name}' already exists.")
        return 
        es.indices.delete(index=index_name, )
        es.indices.create(index=index_name, body=index_body)
        

    # generator
    def generate_actions():
        with open(file_path) as f:
            for line in tqdm(f.readlines()):
                line_json = json.loads(line)
                es_doc = {
                    "content": line_json['content'],
                    "id": line_json['id'],
                }
                es.create(index=index_name, id=line_json['id'], body=es_doc)

    generate_actions()


if __name__ == '__main__':
    build_elasticsearch(index_name='corpus.en', file_path='../corpus.en.jsonl')
