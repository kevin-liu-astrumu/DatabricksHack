import os

params = {
    "chunk_sizes": [256, 512],
    "top_k": 5,
    "template_dir": os.path.join(os.getcwd(), "rag_modules/prompts"),
    "template_file": "query_template.jinja",
}
