"""Utility functions for HerHaq chatbot."""

import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Any
import yaml


def setup_logging(log_file: str = "chatbot.log", level: str = "INFO"):
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


def load_config(config_path: str = "config.yaml") -> Dict:
    """Load configuration from YAML file."""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # Environment variable overrides for deployment platforms (e.g., Render).
    use_ollama = os.getenv("USE_OLLAMA")
    if use_ollama is not None:
        config['llm']['use_ollama'] = use_ollama.strip().lower() in {"1", "true", "yes", "on"}

    ollama_base_url = os.getenv("OLLAMA_BASE_URL")
    if ollama_base_url:
        config['llm']['ollama_base_url'] = ollama_base_url.strip()

    hf_model_name = os.getenv("HF_MODEL_NAME")
    if hf_model_name:
        config['llm']['model_name'] = hf_model_name.strip()

    return config


def load_json_file(file_path: str) -> List[Dict]:
    """Load JSON file with error handling."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else [data]
    except json.JSONDecodeError as e:
        logging.error(f"Error loading {file_path}: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error loading {file_path}: {e}")
        return []


def save_json_file(data: Any, file_path: str):
    """Save data to JSON file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def create_directories(config: Dict):
    """Create necessary directories."""
    dirs = [
        config['data']['processed_dir'],
        config['data']['embeddings_dir'],
        'logs'
    ]
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)


def format_source_citation(source: Dict) -> str:
    """Format source information for citation."""
    source_type = source.get('source_type', 'Unknown')
    source_name = source.get('source_name', 'Unknown')
    reference = source.get('reference', '')
    
    if source_type == 'Legislation' or source_type == 'Pakistani Laws':
        return f"**{source_name}** ({reference})" if reference else f"**{source_name}**"
    elif source_type == 'Hadith':
        return f"**{source_name}** - {reference}" if reference else f"**{source_name}**"
    elif 'Case Study' in source_type or source.get('title'):
        title = source.get('title', 'Case Study')
        year = source.get('year', '')
        return f"**Case Study**: {title} ({year})" if year else f"**Case Study**: {title}"
    else:
        return f"**{source_name}**"


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = ' '.join(text.split())
    
    # Remove special characters but keep punctuation
    # text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\"\']+', '', text)
    
    return text.strip()


def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncate text to maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def extract_keywords(text: str, max_keywords: int = 5) -> List[str]:
    """Extract keywords from text (simple implementation)."""
    # This is a simple implementation; can be enhanced with NLP
    words = text.lower().split()
    # Filter common words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    keywords = [w for w in words if w not in stop_words and len(w) > 3]
    return list(set(keywords))[:max_keywords]
