from jinja2 import Environment, FileSystemLoader
from llama_index.core import PromptTemplate, StorageContext, VectorStoreIndex
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import AutoMergingRetriever
from llama_index.core.storage.docstore import SimpleDocumentStore


def construct_index(llm, nodes, leaf_nodes):
    docstore = SimpleDocumentStore()
    docstore.add_documents(nodes)
    storage_context = StorageContext.from_defaults(docstore=docstore)
    base_index = VectorStoreIndex(leaf_nodes, storage_context=storage_context, llm=llm)
    return storage_context, base_index


def construct_retriever(storage_context, index, top_k):
    base_retriever = index.as_retriever(similarity_top_k=top_k)
    retriever = AutoMergingRetriever(base_retriever, storage_context)
    return retriever


def construct_queryengine(retriever, template_dir, template_file):
    query_engine = RetrieverQueryEngine.from_args(retriever)
    template_loader = FileSystemLoader(template_dir)
    template_env = Environment(loader=template_loader)
    template = template_env.get_template(template_file)

    query_prompt = PromptTemplate(template.render())
    query_engine.update_prompts({"response_synthesizer:text_qa_template": query_prompt})
    return query_engine
