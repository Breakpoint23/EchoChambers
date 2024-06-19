import os

from typing import Literal, Optional, Tuple

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


def main():

    os.environ["GROQ_API_KEY"] = "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"







"""
1. Yes and No question
2. Summaraization
3. Comparision
4. Cause and Effect
5. Problem and Solution


"""


