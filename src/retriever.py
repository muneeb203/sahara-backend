"""Retrieval module for semantic search."""

import logging
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer
import numpy as np

from vector_store import VectorStore
from utils import load_config, format_source_citation


logger = logging.getLogger(__name__)


class Retriever:
    """Semantic retrieval using embeddings and FAISS."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.vector_store = VectorStore(config)
        self.vector_store.load_index()
        
        # Load embedding model for query encoding
        model_name = config['embedding']['model_name']
        logger.info(f"Loading embedding model for queries: {model_name}")
        self.embedding_model = SentenceTransformer(model_name)
        
        self.top_k = config['retrieval']['top_k']
        self.score_threshold = config['retrieval']['score_threshold']
    
    def encode_query(self, query: str) -> np.ndarray:
        """Encode query into embedding."""
        embedding = self.embedding_model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        return embedding
    
    def retrieve(self, query: str, top_k: int = None) -> List[Tuple[Dict, float]]:
        """Retrieve relevant chunks for a query."""
        if top_k is None:
            top_k = self.top_k
        
        # Encode query
        query_embedding = self.encode_query(query)
        
        # Search vector store
        results = self.vector_store.search(query_embedding, top_k=top_k)
        
        # Filter by score threshold
        filtered_results = [
            (chunk, score) for chunk, score in results
            if score >= self.score_threshold
        ]
        
        logger.info(f"Retrieved {len(filtered_results)} chunks above threshold {self.score_threshold}")
        
        return filtered_results
    
    def format_context(self, results: List[Tuple[Dict, float]]) -> str:
        """Format retrieved chunks into context string."""
        if not results:
            return "No relevant information found in the knowledge base."
        
        context_parts = []
        
        for idx, (chunk, score) in enumerate(results, 1):
            metadata = chunk['metadata']
            text = chunk['text']
            
            # Format source citation
            citation = format_source_citation(metadata)
            
            # Build context entry
            context_entry = f"[Source {idx}] {citation}\n{text}\n"
            context_parts.append(context_entry)
        
        return "\n".join(context_parts)
    
    def retrieve_with_context(self, query: str, top_k: int = None) -> Tuple[str, List[Dict]]:
        """Retrieve and format context for LLM."""
        results = self.retrieve(query, top_k)
        context = self.format_context(results)
        
        # Extract sources for citation
        sources = []
        for chunk, score in results:
            source_info = {
                'citation': format_source_citation(chunk['metadata']),
                'score': score,
                'metadata': chunk['metadata']
            }
            sources.append(source_info)
        
        return context, sources


def main():
    """Test retrieval."""
    logging.basicConfig(level=logging.INFO)
    
    config = load_config()
    retriever = Retriever(config)
    
    # Test queries
    test_queries = [
        "What are women's inheritance rights in Pakistan?",
        "How can I file a harassment complaint at work?",
        "What does Islam say about divorce?",
        "Can my husband take a second wife without my permission?"
    ]
    
    for query in test_queries:
        print(f"\n{'='*80}")
        print(f"Query: {query}")
        print(f"{'='*80}")
        
        context, sources = retriever.retrieve_with_context(query)
        
        print("\nRetrieved Context:")
        print(context)
        
        print("\nSources:")
        for source in sources:
            print(f"- {source['citation']} (Score: {source['score']:.3f})")


if __name__ == "__main__":
    main()
