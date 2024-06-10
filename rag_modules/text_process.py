import pymupdf4llm
from llama_index.core import Document
from llama_index.core.node_parser import HierarchicalNodeParser, get_leaf_nodes


def parse_pdf(pdf_file):
    output = pymupdf4llm.to_markdown(pdf_file)
    return output


def text_splitter(text, chunk_sizes=[1024, 512]):
    docs = [Document(text=text)]
    node_parser = HierarchicalNodeParser.from_defaults(chunk_sizes=chunk_sizes)
    nodes = node_parser.get_nodes_from_documents(docs)
    leaf_nodes = get_leaf_nodes(nodes)
    return nodes, leaf_nodes