import torch
import numpy as np
from sentence_transformers import SentenceTransformer, util
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from pydantic import Field
from typing import List


class FinSeerRetriever(BaseRetriever):
    """LangChain-compatible retriever wrapping the FinSeer embedding model."""

    model: SentenceTransformer = Field(exclude=True)
    documents: List[Document] = Field(default_factory=list)
    top_k: int = 3

    class Config:
        arbitrary_types_allowed = True

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        if not self.documents:
            return []

        # Embed query and all docs
        query_emb = self.model.encode(query, convert_to_tensor=True)
        doc_texts = [doc.page_content for doc in self.documents]
        doc_embs = self.model.encode(doc_texts, convert_to_tensor=True)

        # Cosine similarity — find top_k most similar
        scores = util.cos_sim(query_emb, doc_embs)[0]
        top_results = torch.topk(scores, k=min(self.top_k, len(self.documents)))

        # Return matched documents with similarity score in metadata
        matched = []
        for score, idx in zip(top_results.values, top_results.indices):
            doc = self.documents[idx.item()]
            doc.metadata["similarity_score"] = round(score.item(), 4)
            matched.append(doc)

        return matched

    def add_documents(self, docs: List[Document]):
        """Add documents to the retriever's knowledge base."""
        self.documents.extend(docs)


def load_finseer(model_path: str = "../models/finseer", top_k: int = 3) -> FinSeerRetriever:
    """Load FinSeer and return a LangChain-compatible retriever."""
    print(f"Loading FinSeer from {model_path}...")
    model = SentenceTransformer(model_path)
    print("FinSeer loaded!")
    return FinSeerRetriever(model=model, top_k=top_k)