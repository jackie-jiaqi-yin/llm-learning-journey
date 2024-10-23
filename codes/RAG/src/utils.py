from dotenv import load_dotenv
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
import os
from typing import Tuple
from llama_index.core import Settings

def load_llm_config():
    load_dotenv()
    embedding_model = AzureOpenAIEmbedding(
        model= os.getenv("EMBEDDING_MODEL"),
        engine = os.getenv("EMBEDDING_ENGINE"),
        api_key = os.getenv("AZURE_OPENAI_KEY"),
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version = os.getenv("EMBEDDING_API_VERSION")
    )

    llm = AzureOpenAI(
        model = os.getenv("LLM_MODEL"),
        engine = os.getenv("LLM_ENGINE"),
        api_key = os.getenv("AZURE_OPENAI_KEY"),
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version = os.getenv("LLM_API_VERSION")
    )
    Settings.llm = llm
    Settings.embed_model = embedding_model