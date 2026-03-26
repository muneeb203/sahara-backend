"""Embedding generation module using sentence transformers."""

import logging
import numpy as np
import torch
from pathlib import Path
from typing import List, Dict
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

from utils import load_config, load_json_file, save_json_file, create_directories


logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """Generate embeddings for text chunks."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.processed_dir = Path(config['data']['processed_dir'])
        self.embeddings_dir = Path(config['data']['embeddings_dir'])
        
        # Load embedding model
        model_name = config['embedding']['model_name']
        device = config['embedding']['device']
        
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        
        # Set device
        if device == 'cuda' and torch.cuda.is_available():
            self.device = 'cuda'
            self.model = self.model.to('cuda')
            logger.info("Using CUDA for embeddings")
        else:
            self.device = 'cpu'
            logger.info("Using CPU for embeddings")
        
        self.batch_size = config['embedding']['batch_size']
        self.max_length = config['embedding']['max_length']
        
        create_directories(config)
    
    def load_chunks(self) -> List[Dict]:
        """Load processed chunks."""
        chunks_file = self.processed_dir / "processed_chunks.json"
        logger.info(f"Loading chunks from {chunks_file}")
        return load_json_file(str(chunks_file))
    
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts."""
        embeddings = self.model.encode(
            texts,
            batch_size=self.batch_size,
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        return embeddings
    
    def process_chunks(self, chunks: List[Dict]) -> tuple:
        """Generate embeddings for all chunks."""
        logger.info(f"Generating embeddings for {len(chunks)} chunks...")
        
        # Extract texts
        texts = [chunk['text'] for chunk in chunks]
        
        # Generate embeddings in batches
        all_embeddings = []
        
        for i in tqdm(range(0, len(texts), self.batch_size), desc="Generating embeddings"):
            batch_texts = texts[i:i + self.batch_size]
            batch_embeddings = self.generate_embeddings(batch_texts)
            all_embeddings.append(batch_embeddings)
        
        # Concatenate all embeddings
        embeddings = np.vstack(all_embeddings)
        
        logger.info(f"Generated embeddings shape: {embeddings.shape}")
        
        return embeddings, chunks
    
    def save_embeddings(self, embeddings: np.ndarray, chunks: List[Dict]):
        """Save embeddings and metadata."""
        # Save embeddings as numpy array
        embeddings_file = self.embeddings_dir / "embeddings.npy"
        np.save(str(embeddings_file), embeddings)
        logger.info(f"Saved embeddings to {embeddings_file}")
        
        # Save chunks metadata (without embeddings to save space)
        metadata_file = self.embeddings_dir / "chunks_metadata.json"
        save_json_file(chunks, str(metadata_file))
        logger.info(f"Saved metadata to {metadata_file}")
        
        # Save embedding info
        info = {
            'model_name': self.config['embedding']['model_name'],
            'embedding_dim': embeddings.shape[1],
            'num_chunks': embeddings.shape[0],
            'device': self.device
        }
        info_file = self.embeddings_dir / "embedding_info.json"
        save_json_file(info, str(info_file))
        logger.info(f"Saved embedding info to {info_file}")


def main():
    """Main embedding generation function."""
    logging.basicConfig(level=logging.INFO)
    
    config = load_config()
    generator = EmbeddingGenerator(config)
    
    # Load chunks
    chunks = generator.load_chunks()
    
    # Generate embeddings
    embeddings, chunks = generator.process_chunks(chunks)
    
    # Save results
    generator.save_embeddings(embeddings, chunks)
    
    logger.info("Embedding generation complete!")


if __name__ == "__main__":
    main()
