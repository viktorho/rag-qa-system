from elasticsearch import Elasticsearch
from config import config

es = Elasticsearch(f'http://localhost:{config["port"]}',)

def es_search(search_query, es):
  response = es.search(index=f"corpus.{config['language']}", body=search_query, size=5,)
  return response

if __name__ == '__main__':
  for search_query in [
    {"query": {
        "match": {
          "content": {"query": "Will a theft stealing someone else's property result in being arrested and sentenced?",
                      "fuzziness": "AUTO"}
        }
      }},
      {"query": {
        "match": {
          "content": {"query": "What are the circumstances that lead to aggravated punishment for theft?",
                      "fuzziness": "AUTO"}
        }
      }},
      {"query": {
          "match": {
            "content": {"query": "What impact does a prior theft record have on being caught stealing again?",
                        "fuzziness": "AUTO"}
          }
        }
      }]:

    response = es_search(search_query, es)

    print("Search results:")
    for hit in response['hits']['hits']:
        print(hit["_source"]['id'], end='\t')
    print('\n')
