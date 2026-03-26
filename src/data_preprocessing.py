"""Data preprocessing module for HerHaq dataset."""

import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple
from tqdm import tqdm
import re

from utils import load_config, load_json_file, save_json_file, clean_text, create_directories


logger = logging.getLogger(__name__)


class DataPreprocessor:
    """Preprocess HerHaq dataset for RAG pipeline."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.source_dir = Path(config['data']['source_dir'])
        self.processed_dir = Path(config['data']['processed_dir'])
        self.chunk_size = config['chunking']['chunk_size']
        self.chunk_overlap = config['chunking']['chunk_overlap']
        self.min_chunk_size = config['chunking']['min_chunk_size']
        
        create_directories(config)
    
    def load_all_data(self) -> Dict[str, List[Dict]]:
        """Load all dataset files."""
        logger.info("Loading dataset files...")
        
        data = {
            'laws': [],
            'case_studies': [],
            'ahadith': []
        }
        
        # Load laws
        for file_name in self.config['dataset_files']['laws']:
            file_path = self.source_dir / file_name
            if file_path.exists():
                items = load_json_file(str(file_path))
                data['laws'].extend(items)
                logger.info(f"Loaded {len(items)} items from {file_name}")
        
        # Load case studies
        for file_name in self.config['dataset_files']['case_studies']:
            file_path = self.source_dir / file_name
            if file_path.exists():
                items = load_json_file(str(file_path))
                data['case_studies'].extend(items)
                logger.info(f"Loaded {len(items)} items from {file_name}")
        
        # Load ahadith
        for file_name in self.config['dataset_files']['ahadith']:
            file_path = self.source_dir / file_name
            if file_path.exists():
                items = load_json_file(str(file_path))
                data['ahadith'].extend(items)
                logger.info(f"Loaded {len(items)} items from {file_name}")
        
        logger.info(f"Total loaded - Laws: {len(data['laws'])}, "
                   f"Case Studies: {len(data['case_studies'])}, "
                   f"Ahadith: {len(data['ahadith'])}")
        
        return data
    
    def clean_item(self, item: Dict, source_type: str) -> Dict:
        """Clean individual data item."""
        cleaned = {}
        
        # Common fields
        cleaned['source_type'] = source_type
        cleaned['text'] = clean_text(item.get('text', ''))
        cleaned['source_name'] = item.get('source_name', 'Unknown')
        cleaned['reference'] = item.get('reference', '')
        cleaned['category'] = item.get('category', 'General')
        cleaned['country'] = item.get('country', 'Pakistan')
        
        # Type-specific fields
        if source_type == 'law':
            cleaned['theme_tags'] = item.get('theme_tags', [])
            cleaned['relevance_score'] = item.get('relevance_score', 0.5)
        
        elif source_type == 'case_study':
            cleaned['title'] = item.get('title', '')
            cleaned['year'] = item.get('year', '')
            cleaned['summary'] = clean_text(item.get('summary', ''))
            cleaned['facts'] = item.get('facts', [])
            cleaned['legal_issues'] = item.get('legal_issues', [])
            cleaned['ruling_or_outcome'] = clean_text(item.get('ruling_or_outcome', ''))
            cleaned['keywords'] = item.get('keywords', [])
        
        elif source_type == 'hadith':
            cleaned['translation'] = clean_text(item.get('translation', ''))
            cleaned['theme_tags'] = item.get('theme_tags', [])
            cleaned['relevance_score'] = item.get('relevance_score', 0.5)
        
        return cleaned
    
    def create_chunks(self, text: str, metadata: Dict) -> List[Dict]:
        """Split text into overlapping chunks."""
        if not text or len(text) < self.min_chunk_size:
            return []
        
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = ' '.join(chunk_words)
            
            if len(chunk_text) >= self.min_chunk_size:
                chunk = {
                    'text': chunk_text,
                    'metadata': metadata.copy(),
                    'chunk_index': len(chunks)
                }
                chunks.append(chunk)
        
        return chunks
    
    def process_law(self, item: Dict) -> List[Dict]:
        """Process a law item into chunks."""
        cleaned = self.clean_item(item, 'law')
        
        # For laws, each item is typically self-contained
        metadata = {
            'source_type': 'law',
            'source_name': cleaned['source_name'],
            'reference': cleaned['reference'],
            'category': cleaned['category'],
            'theme_tags': cleaned['theme_tags']
        }
        
        return [{
            'text': cleaned['text'],
            'metadata': metadata,
            'chunk_index': 0
        }]
    
    def process_case_study(self, item: Dict) -> List[Dict]:
        """Process a case study into chunks."""
        cleaned = self.clean_item(item, 'case_study')
        
        # Combine all case study information
        full_text = f"{cleaned['title']}\n\n"
        full_text += f"Summary: {cleaned['summary']}\n\n"
        
        if cleaned['facts']:
            full_text += "Facts:\n" + "\n".join(f"- {fact}" for fact in cleaned['facts']) + "\n\n"
        
        if cleaned['legal_issues']:
            full_text += "Legal Issues:\n" + "\n".join(f"- {issue}" for issue in cleaned['legal_issues']) + "\n\n"
        
        full_text += f"Outcome: {cleaned['ruling_or_outcome']}"
        
        metadata = {
            'source_type': 'case_study',
            'title': cleaned['title'],
            'year': cleaned['year'],
            'keywords': cleaned['keywords']
        }
        
        return self.create_chunks(full_text, metadata)
    
    def process_hadith(self, item: Dict) -> List[Dict]:
        """Process a hadith into chunks."""
        cleaned = self.clean_item(item, 'hadith')
        
        # Use translation if available, otherwise use text
        text = cleaned.get('translation') or cleaned['text']
        
        metadata = {
            'source_type': 'hadith',
            'source_name': cleaned['source_name'],
            'reference': cleaned['reference'],
            'category': cleaned['category'],
            'theme_tags': cleaned['theme_tags']
        }
        
        return [{
            'text': text,
            'metadata': metadata,
            'chunk_index': 0
        }]
    
    def process_all_data(self) -> List[Dict]:
        """Process all data into chunks."""
        logger.info("Processing all data...")
        
        data = self.load_all_data()
        all_chunks = []
        
        # Process laws
        logger.info("Processing laws...")
        for item in tqdm(data['laws'], desc="Laws"):
            chunks = self.process_law(item)
            all_chunks.extend(chunks)
        
        # Process case studies
        logger.info("Processing case studies...")
        for item in tqdm(data['case_studies'], desc="Case Studies"):
            chunks = self.process_case_study(item)
            all_chunks.extend(chunks)
        
        # Process ahadith
        logger.info("Processing ahadith...")
        for item in tqdm(data['ahadith'], desc="Ahadith"):
            chunks = self.process_hadith(item)
            all_chunks.extend(chunks)
        
        # Add unique IDs
        for idx, chunk in enumerate(all_chunks):
            chunk['id'] = f"chunk_{idx}"
        
        logger.info(f"Created {len(all_chunks)} chunks")
        
        return all_chunks
    
    def save_processed_data(self, chunks: List[Dict]):
        """Save processed chunks to file."""
        output_file = self.processed_dir / "processed_chunks.json"
        save_json_file(chunks, str(output_file))
        logger.info(f"Saved {len(chunks)} chunks to {output_file}")
        
        # Save statistics
        stats = {
            'total_chunks': len(chunks),
            'by_source_type': {}
        }
        
        for chunk in chunks:
            source_type = chunk['metadata']['source_type']
            stats['by_source_type'][source_type] = stats['by_source_type'].get(source_type, 0) + 1
        
        stats_file = self.processed_dir / "processing_stats.json"
        save_json_file(stats, str(stats_file))
        logger.info(f"Saved statistics to {stats_file}")


def main():
    """Main preprocessing function."""
    logging.basicConfig(level=logging.INFO)
    
    config = load_config()
    preprocessor = DataPreprocessor(config)
    
    chunks = preprocessor.process_all_data()
    preprocessor.save_processed_data(chunks)
    
    logger.info("Preprocessing complete!")


if __name__ == "__main__":
    main()
