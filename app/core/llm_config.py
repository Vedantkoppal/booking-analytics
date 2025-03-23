# LLM Config

from sqlalchemy import create_engine
from llama_index.core import SQLDatabase
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.query_engine import NLSQLTableQueryEngine
from app.core.data_config import DB_URI

# llm instance
llm = Ollama(model="phi4-mini:latest",temperature=0.0,request_timeout=200)  # kept timeout to 200 because of CPU limitations
embed_model = HuggingFaceEmbedding(model_name="all-MiniLM-L6-v2")


# OpenAI Settings for LLM : uncomment for opeanai model
# import os
# import openai

# os.environ["OPENAI_API_KEY"] = "sk-../"
# openai.api_key = os.environ["OPENAI_API_KEY"]
# llm = Ollama(model="gpt-3.5-turbo", temperature=0.0, request_timeout=200)


# engine to connect to db
engine_llm = create_engine(DB_URI)
sql_database = SQLDatabase(
    engine=engine_llm
    )


# llm-db core engine
query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database,
    llm=llm,
    embed_model=embed_model,
    timeout=200
)

    
