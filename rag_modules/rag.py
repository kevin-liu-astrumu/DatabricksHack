from rag_modules.index_store import (
    construct_index,
    construct_queryengine,
    construct_retriever,
)
from rag_modules.text_process import parse_pdf, text_splitter


class RAG:

    def __init__(self, pdf_file, llm, params):
        self.pdf_file = pdf_file
        self.llm = llm
        self.params = params
        self.setup_queryengine()

    def process_pdf(self):
        parsed_text = parse_pdf(self.pdf_file)
        self.nodes, self.leaf_nodes = text_splitter(
            parsed_text, self.params["chunk_sizes"]
        )

    def setup_queryengine(self):
        self.process_pdf()
        storage_context, base_index = construct_index(
            self.llm, self.nodes, self.leaf_nodes
        )
        retriever = construct_retriever(
            storage_context, base_index, self.params["top_k"]
        )
        self.query_engine = construct_queryengine(
            retriever, self.params["template_dir"], self.params["template_file"]
        )

    def respond_query(self, query):
        return self.query_engine.query(query)
