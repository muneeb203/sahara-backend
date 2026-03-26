"""Test script for the complete RAG pipeline."""

import sys
from pathlib import Path
import logging

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from utils import load_config, setup_logging
from retriever import Retriever


def test_retrieval():
    """Test retrieval component."""
    print("\n" + "="*80)
    print("Testing Retrieval Component")
    print("="*80)
    
    config = load_config()
    retriever = Retriever(config)
    
    test_queries = [
        "What are women's inheritance rights in Pakistan?",
        "How can I file a harassment complaint at work?",
        "What does Islam say about divorce?",
        "Can my husband take a second wife without my permission?",
        "What are the penalties for domestic violence?"
    ]
    
    for query in test_queries:
        print(f"\n{'─'*80}")
        print(f"Query: {query}")
        print(f"{'─'*80}")
        
        context, sources = retriever.retrieve_with_context(query, top_k=3)
        
        print("\nTop 3 Retrieved Sources:")
        for idx, source in enumerate(sources, 1):
            print(f"\n{idx}. {source['citation']}")
            print(f"   Relevance Score: {source['score']:.3f}")
            print(f"   Type: {source['metadata']['source_type']}")
        
        print("\n" + "─"*80)


def test_sample_queries():
    """Test with sample queries."""
    print("\n" + "="*80)
    print("Sample Query Testing")
    print("="*80)
    
    from chatbot import HerHaqChatbot
    
    config = load_config()
    chatbot = HerHaqChatbot(config)
    
    sample_queries = [
        {
            "query": "What are my rights if my husband wants to marry another woman?",
            "expected_topics": ["polygamy", "permission", "arbitration council", "dower"]
        },
        {
            "query": "How do I inherit property from my father?",
            "expected_topics": ["inheritance", "Islamic law", "share", "property"]
        },
        {
            "query": "My boss is harassing me at work. What can I do?",
            "expected_topics": ["harassment", "workplace", "complaint", "inquiry committee"]
        }
    ]
    
    for idx, test_case in enumerate(sample_queries, 1):
        print(f"\n{'='*80}")
        print(f"Test Case {idx}")
        print(f"{'='*80}")
        print(f"Query: {test_case['query']}")
        print(f"Expected Topics: {', '.join(test_case['expected_topics'])}")
        
        result = chatbot.chat(test_case['query'])
        
        print(f"\nResponse:")
        print(result['response'])
        
        print(f"\nSources Used:")
        for source in result['sources']:
            print(f"  - {source['citation']}")
        
        print("\n" + "="*80)


def test_statistics():
    """Display dataset statistics."""
    print("\n" + "="*80)
    print("Dataset Statistics")
    print("="*80)
    
    from utils import load_json_file
    
    config = load_config()
    
    # Load processed chunks
    chunks_file = Path(config['data']['processed_dir']) / "processed_chunks.json"
    if chunks_file.exists():
        chunks = load_json_file(str(chunks_file))
        
        print(f"\nTotal Chunks: {len(chunks)}")
        
        # Count by source type
        source_types = {}
        for chunk in chunks:
            source_type = chunk['metadata']['source_type']
            source_types[source_type] = source_types.get(source_type, 0) + 1
        
        print("\nChunks by Source Type:")
        for source_type, count in sorted(source_types.items()):
            print(f"  {source_type}: {count}")
        
        # Sample chunks
        print("\nSample Chunks:")
        for i in range(min(3, len(chunks))):
            chunk = chunks[i]
            print(f"\n{i+1}. Type: {chunk['metadata']['source_type']}")
            print(f"   Text: {chunk['text'][:200]}...")
    else:
        print("\nProcessed chunks not found. Run data_preprocessing.py first.")
    
    print("\n" + "="*80)


def main():
    """Run all tests."""
    setup_logging(level="INFO")
    
    print("\n" + "="*80)
    print("HerHaq Chatbot - Pipeline Testing")
    print("="*80)
    
    try:
        # Test 1: Statistics
        test_statistics()
        
        # Test 2: Retrieval
        test_retrieval()
        
        # Test 3: Sample queries (optional - requires LLaMA model)
        print("\n" + "="*80)
        print("Full Pipeline Test (with LLM)")
        print("="*80)
        response = input("\nRun full pipeline test with LLM? This requires LLaMA 3B to be loaded. (y/n): ")
        
        if response.lower() == 'y':
            test_sample_queries()
        else:
            print("\nSkipping full pipeline test.")
        
        print("\n" + "="*80)
        print("Testing Complete!")
        print("="*80)
    
    except Exception as e:
        logging.error(f"Test failed: {e}")
        raise


if __name__ == "__main__":
    main()
