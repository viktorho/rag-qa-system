from utils_eval import BLEU, METEOR, BERTSCORE
import pandas as pd
import numpy as np

def load_metric():
    metrics = {}
    metrics["BLEU"] = BLEU(n = 1)
    # metrics["BERTSCORE"] = BERTSCORE()
    return metrics

def recall_at_k(ground_truth, predictions, k=3):
    assert len(ground_truth) == len(predictions)
    total_recall = 0
    for actual, predicted in zip(ground_truth, predictions):
        if len(predicted) > k:
            predicted = predicted[:k]
        relevant_and_retrieved = [item for item in predicted if item in actual]
        recall = len(relevant_and_retrieved) / len(actual) if actual else 0
        total_recall += recall

    return total_recall / len(ground_truth)

if __name__ == '__main__':
    metrics = load_metric()
    out_path = '../example.en.out.csv'
    ref_path = '../example.en.csv'
    out = pd.read_csv(out_path, index_col=None, sep='|')
    ref = pd.read_csv(ref_path, index_col=None, sep='|')
    for k in metrics.keys():
        score = metrics[k].score([item.split() for item in ref['answer']], [item.split() for item in out['answer']])
        print(k, np.mean(score))
    print("recall_at_3", recall_at_k(ref['id'], out['id']))

