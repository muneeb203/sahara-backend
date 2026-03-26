"""FAISS vector store for semantic search."""

import logging
import numpy as np
import faiss
from pathlib import Path
from typing import List, Dict, Tuple

from utils import load_config, load_json_file, save_json_file


logger = logging.getLogger(__name__)


class VectorStore:
    """FAISS-based vector store for semantic search."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.embeddings_dir = Path(config['data']['embeddings_dir'])
        self.dimension = config['vector_store']['dimension']
        self.index = None
        self.chunks = None
        
    def build_index(self):
        """Build FAISS index from embeddings."""
        logger.info("Building FAISS index...")
        
        # Load embeddings
        embeddings_file = self.embeddings_dir / "embeddings.npy"
        embeddings = np.load(str(embeddings_file))
        
        # Load metadata
        metadata_file = self.embeddings_dir / "chunks_metadata.json"
        self.chunks = load_json_file(str(metadata_file))
        
        logger.info(f"Loaded {len(embeddings)} embeddings with dimension {embeddings.shape[1]}")
        
        # Create FAISS index
        # Using IndexFlatL2 for exact search (can be changed to IndexIVFFlat for faster approximate search)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        
        # Add embeddings to index
        self.index.add(embeddings.astype('float32'))
        
        logger.info(f"Built FAISS index with {self.index.ntotal} vectors")
        
    def save_index(self):
        """Save FAISS index to disk."""
        if self.index is None:
            raise ValueError("Index not built yet")
        
        index_file = self.embeddings_dir / "faiss_index.bin"
        faiss.write_index(self.index, str(index_file))
        logger.info(f"Saved FAISS index to {index_file}")
    
    def load_index(self):
        """Load FAISS index from disk."""
        index_file = self.embeddings_dir / "faiss_index.bin"
        
        if not index_file.exists():
            logger.warning("Index file not found, building new index...")
            self.build_index()
            self.save_index()
            return
        
        logger.info(f"Loading FAISS index from {index_file}")
        self.index = faiss.read_index(str(index_file))
        
        # Load metadata
        metadata_file = self.embeddings_dir / "chunks_metadata.json"
        self.chunks = load_json_file(str(metadata_file))
        
        logger.info(f"Loaded FAISS index with {self.index.ntotal} vectors")
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[Dict, float]]:
        """Search for similar chunks."""
        if self.index is None:
            self.load_index()
        
        # Ensure query is 2D array
        if len(query_embedding.shape) == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        # Search
        distances, indices = self.index.search(query_embedding.astype('float32'), top_k)
        
        # Get results
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.chunks):
                chunk = self.chunks[idx]
                # Convert L2 distance to similarity score (lower is better, so invert)
                similarity = 1 / (1 + distance)
                results.append((chunk, similarity))
        
        return results
    
    def get_chunk_by_id(self, chunk_id: str) -> Dict:
        """Get chunk by ID."""
        if self.chunks is None:
            self.load_index()
        
        for chunk in self.chunks:
            if chunk['id'] == chunk_id:
                return chunk
        
        return None


def main():
    """Build and save FAISS index."""
    logging.basicConfig(level=logging.INFO)
    
    config = load_config()
    vector_store = VectorStore(config)
    
    # Build and save index
    vector_store.build_index()
    vector_store.save_index()
    
    logger.info("Vector store creation complete!")


if __name__ == "__main__":
    main()
