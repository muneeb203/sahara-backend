"""Test the retrieval system without LLM - see what the chatbot finds."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "src"))

from retriever import Retriever
from utils import load_config, setup_logging

def main():
    """Test retrieval with sample queries."""
    setup_logging(level="INFO")
    
    print("\n" + "="*80)
    print("  HerHaq Chatbot - Retrieval System Demo")
    print("  (Testing without LLM - showing what sources are found)")
    print("="*80)
    
    config = load_config()
    retriever = Retriever(config)
    
    # Sample queries
    queries = [
        "What are my inheritance rights as a daughter in Pakistan?",
        "How can I file a harassment complaint at work?",
        "Can my husband divorce me without my consent?",
        "What does Islam say about women's property rights?",
        "Can my husband marry another woman without telling me?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{'='*80}")
        print(f"Query {i}: {query}")
        print(f"{'='*80}\n")
        
        # Retrieve context
        context, sources = retriever.retrieve_with_context(query, top_k=3)
        
        print("📚 Retrieved Sources:\n")
        for idx, source in enumerate(sources, 1):
            print(f"{idx}. {source['citation']}")
            print(f"   Relevance: {source['score']:.3f}")
            print(f"   Type: {source['metadata']['source_type']}")
            print()
        
        print("📄 Context Preview:")
        print("-" * 80)
        # Show first 500 characters of context
        preview = context[:500] + "..." if len(context) > 500 else context
        print(preview)
        print("-" * 80)
        
        input("\nPress Enter to see next query...")
    
    print("\n" + "="*80)
    print("  Demo Complete!")
    print("="*80)
    print("\nThis shows what information the chatbot finds for each query.")
    print("Once LLM is set up, it will use this context to generate responses.")
    print("\nTo set up LLM:")
    print("  1. Open a new terminal")
    print("  2. Run: ollama pull llama3")
    print("  3. Then run: streamlit run app.py")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
