"""OpenAI adapter. The only module that constructs model clients."""

from __future__ import annotations

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from config import Settings


def chat_model(settings: Settings) -> ChatOpenAI:
    kwargs: dict = {
        "model": settings.openai_model,
        "api_key": settings.openai_api_key or None,
        "timeout": 30,
        "max_retries": 2,
    }
    if settings.openai_reasoning_effort:
        kwargs["reasoning_effort"] = settings.openai_reasoning_effort
    return ChatOpenAI(**kwargs)


def structured(settings: Settings, schema: type):
    # function_calling tolerates optional fields and defaults; strict json_schema rejects them.
    return chat_model(settings).with_structured_output(schema, method="function_calling")


def embeddings(settings: Settings) -> OpenAIEmbeddings:
    return OpenAIEmbeddings(model=settings.embedding_model, api_key=settings.openai_api_key or None)
