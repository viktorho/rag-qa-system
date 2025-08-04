from es_build import build_elasticsearch
from es_search import es_search, es
from prompt_generation import get_response, client,clarify_prompt
import pandas as pd
from config import config

if __name__ == '__main__':
    # building index
    build_elasticsearch(index_name=f'corpus.{config["language"]}', file_path=f'../corpus.{config["language"]}.jsonl')

    # load data
    df = pd.read_csv(f'../{config["task-type"]}.{config["language"]}.csv', index_col=None, sep='|')
    df_out = df.copy()
    df_out['id'] = df_out['id'].astype(str)
    df_out['answer'] = df_out['answer'].astype(str)
    df_out['reference'] = df_out['reference'].astype(str)

    # you can improve the RAG performance by using a better template 
    rag_template = ['Given these Chinese laws: ', 'Please answer the questions: ']

    for i in range(len(df)):
        row = df.iloc[i]

        # construct queries, you can improve the RAG performance by generate a better question instead of using the original question 
        question = row['question']

        search_query = {"query": {
                "match": {
                "content": {"query": question.lower(),

                 "fuzziness": "AUTO"}
                } 
            }
            }

        search_query['query']['match']['content']['query'] = clarify_prompt(search_query,client)
        # search for documents, you can improve the RAG performance by using different hyper parameters in elasticsearch
        response = es_search(search_query, es)
        df_out.loc[i,'id'] = ','.join([str(hit["_source"]['id']) for hit in response['hits']['hits']])
        df_out.loc[i,'reference'] = '\t'.join([hit["_source"]['content'] for hit in response['hits']['hits']])
        # generate response, you can improve the RAG performance by using different RAG methods and prompt construction
        input_prompt = rag_template[0] + df_out.iloc[i]['reference'] + rag_template[1] + row['question']
        
        df_out.loc[i,'answer'] = get_response(input_prompt, client)

    df_out.to_csv(f'../{config["task-type"]}.{config["language"]}.out.csv', sep='|', index=False)

