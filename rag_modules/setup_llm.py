from llama_index.llms.openai import OpenAI


def setup_llm(llm_model="gpt=3.5-turbo"):
    return OpenAI(temperature=0, model="gpt-3.5-turbo")
