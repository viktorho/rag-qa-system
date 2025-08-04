# Retrieval-Augmented QA with GLM-4

A minimal pipeline for question answering that combines Elasticsearch retrieval with ZhipuAI's GLM-4 model. The system indexes a legal corpus, clarifies user queries, retrieves relevant passages, and streams answers from GLM-4.

## Features
- **Elasticsearch BM25 retrieval** over language-specific corpora.
- **Prompt clarification** to rewrite vague questions before search.
- **GLM-4 answer generation** with streaming outputs.
- **Evaluation tools** for BLEU and recall@k.

## Quick Start
1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Start a local Elasticsearch instance (default port `9200`).
2. **Configure** `code/config.json`
   - `api-key`: your ZhipuAI key (do not commit real keys).
   - `language`: `en` or `cn` to pick data files and index name.
   - `task-type`: CSV prefix for tasks (`task` or `example`).
   - `port`: Elasticsearch port.
3. **Run the pipeline**
   ```bash
   python code/main.py
   ```
   The script builds an index, retrieves passages, and saves answers to `{task-type}.{language}.out.csv`.
4. **Evaluate**
   ```bash
   python code/eval.py
   ```
   Prints BLEU and recall@k scores for the generated answers.

## Data Format
Input CSV files use pipe delimiters with the following columns:

| Column | Description |
|---|---|
| `task_id` | Unique question identifier |
| `question` | Natural language query |
| `crime` | (Optional) category label |
| `answer` | Reference answer |
| `reference` | Supporting passages |
| `id` | Document identifiers |

## Customization Tips
- Swap in your own corpus JSONL file and adjust `language`.
- Modify prompt templates in `code/main.py` for new domains.
- Tune Elasticsearch query parameters for better retrieval.

## Contributing
Pull requests are welcome! Please open an issue first to discuss major changes.

## License
This project currently has no license. You are responsible for adding one before redistribution.

