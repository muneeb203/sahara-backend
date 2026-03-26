# HerHaq Chatbot - Technical Documentation

## System Architecture

### Overview

The HerHaq chatbot is a Retrieval-Augmented Generation (RAG) system that combines:
1. **Vector Database**: FAISS for semantic search
2. **Embedding Model**: Sentence Transformers for text encoding
3. **LLM**: LLaMA 3B for response generation
4. **Knowledge Base**: Pakistani laws, case studies, and Islamic ahadith

### Architecture Diagram

```
User Query
    ↓
[Query Encoding] → Sentence Transformer
    ↓
[Semantic Search] → FAISS Vector Store
    ↓
[Context Retrieval] → Top-K Relevant Chunks
    ↓
[Prompt Construction] → System Prompt + Context + Query
    ↓
[Response Generation] → LLaMA 3B
    ↓
[Post-processing] → Add Citations + Safety Checks
    ↓
Final Response
```

## Components

### 1. Data Preprocessing (`data_preprocessing.py`)

**Purpose**: Clean and chunk the raw dataset into retrieval-ready pieces.

**Process**:
1. Load JSON files from FYP_dataset
2. Clean text (remove special characters, normalize spacing)
3. Extract metadata (source, reference, category)
4. Create chunks with overlap for context preservation
5. Save processed chunks with unique IDs

**Key Functions**:
- `load_all_data()`: Load all dataset files
- `clean_item()`: Clean individual data items
- `create_chunks()`: Split text into overlapping chunks
- `process_law()`, `process_case_study()`, `process_hadith()`: Type-specific processing

**Output**:
- `processed_chunks.json`: All chunks with metadata
- `processing_stats.json`: Dataset statistics

### 2. Embedding Generation (`embedding_generator.py`)

**Purpose**: Convert text chunks into dense vector embeddings.

**Model**: `sentence-transformers/all-MiniLM-L6-v2`
- Dimension: 384
- Fast and efficient
- Good balance of speed and quality

**Process**:
1. Load processed chunks
2. Encode text in batches
3. Normalize embeddings (L2 normalization)
4. Save as numpy array

**Key Functions**:
- `generate_embeddings()`: Batch encode texts
- `process_chunks()`: Process all chunks
- `save_embeddings()`: Save embeddings and metadata

**Output**:
- `embeddings.npy`: Dense vector embeddings
- `chunks_metadata.json`: Chunk metadata
- `embedding_info.json`: Model information

### 3. Vector Store (`vector_store.py`)

**Purpose**: Build and manage FAISS index for fast similarity search.

**Index Type**: `IndexFlatL2`
- Exact search (can be changed to approximate for speed)
- L2 distance metric
- No training required

**Process**:
1. Load embeddings from numpy file
2. Create FAISS index
3. Add embeddings to index
4. Save index to disk

**Key Functions**:
- `build_index()`: Create FAISS index
- `search()`: Find similar chunks
- `load_index()`: Load pre-built index

**Output**:
- `faiss_index.bin`: FAISS index file

### 4. Retriever (`retriever.py`)

**Purpose**: Perform semantic search and format context for LLM.

**Process**:
1. Encode user query using same embedding model
2. Search FAISS index for top-K similar chunks
3. Filter by similarity threshold
4. Format results with source citations

**Key Functions**:
- `encode_query()`: Convert query to embedding
- `retrieve()`: Get relevant chunks
- `format_context()`: Format for LLM consumption
- `retrieve_with_context()`: Complete retrieval pipeline

**Parameters**:
- `top_k`: Number of chunks to retrieve (default: 5)
- `score_threshold`: Minimum similarity score (default: 0.3)

### 5. LLM Interface (`llm_interface.py`)

**Purpose**: Interface with LLaMA 3B for response generation.

**Supported Backends**:
1. **Hugging Face Transformers**
   - Direct model loading
   - Quantization support (8-bit, 4-bit)
   - GPU acceleration

2. **Ollama**
   - Easier setup
   - Automatic model management
   - Lower memory usage

**Process**:
1. Load LLaMA 3B model
2. Format prompt with system instructions, context, and query
3. Generate response with controlled parameters
4. Post-process output

**Key Functions**:
- `_init_huggingface()`: Load HF model
- `_init_ollama()`: Initialize Ollama client
- `generate()`: Generate response
- `format_prompt()`: Create LLaMA-compatible prompt

**Generation Parameters**:
- `max_new_tokens`: 512
- `temperature`: 0.7 (controls randomness)
- `top_p`: 0.9 (nucleus sampling)
- `do_sample`: True (enables sampling)

### 6. Chatbot (`chatbot.py`)

**Purpose**: Main RAG pipeline orchestration.

**Process**:
1. Receive user query
2. Perform safety checks
3. Retrieve relevant context
4. Generate response using LLM
5. Add source citations
6. Maintain conversation history

**Key Functions**:
- `chat()`: Main chat function
- `_safety_check()`: Check for dangerous queries
- `_format_response_with_sources()`: Add citations
- `_add_to_history()`: Maintain conversation context

**Safety Features**:
- Crisis detection (suicide, self-harm)
- Automatic helpline suggestions
- Privacy protection

### 7. Web Interface (`app.py`)

**Purpose**: User-friendly Streamlit web interface.

**Features**:
- Chat interface with history
- Source citation display
- Example questions
- Emergency contacts
- Conversation management

**Components**:
- Main chat area
- Sidebar with information
- Message display with formatting
- Source expansion panels

## Data Flow

### Query Processing Flow

```
1. User Input
   ↓
2. Safety Check
   ↓ (if safe)
3. Query Encoding
   - Sentence Transformer
   - 384-dim vector
   ↓
4. Semantic Search
   - FAISS similarity search
   - Top-5 chunks
   - Score filtering
   ↓
5. Context Formatting
   - Add source citations
   - Format for LLM
   ↓
6. Prompt Construction
   - System prompt
   - Retrieved context
   - User query
   ↓
7. LLM Generation
   - LLaMA 3B
   - Temperature: 0.7
   - Max tokens: 512
   ↓
8. Post-processing
   - Add citations
   - Format response
   - Add disclaimer
   ↓
9. Response Display
```

## Dataset Structure

### Input Data Format

#### Laws
```json
{
  "category": "Legal & Testimony Rights",
  "source_type": "Legislation",
  "source_name": "Muslim Family Laws Ordinance, 1961",
  "reference": "Section 6",
  "text": "...",
  "country": "Pakistan",
  "theme_tags": ["marriage", "polygamy"]
}
```

#### Case Studies
```json
{
  "id": "CS-001",
  "title": "...",
  "year": "2017",
  "summary": "...",
  "facts": [...],
  "legal_issues": [...],
  "ruling_or_outcome": "...",
  "keywords": [...]
}
```

#### Ahadith
```json
{
  "category": "Inheritance Rights",
  "source_type": "Hadith",
  "source_name": "Sahih Muslim",
  "reference": "...",
  "text": "...",
  "translation": "...",
  "theme_tags": ["inheritance", "property"]
}
```

### Processed Chunk Format

```json
{
  "id": "chunk_0",
  "text": "...",
  "metadata": {
    "source_type": "law|case_study|hadith",
    "source_name": "...",
    "reference": "...",
    "category": "...",
    "theme_tags": [...]
  },
  "chunk_index": 0
}
```

## Configuration

### Key Configuration Parameters

```yaml
# Embedding
embedding:
  model_name: "sentence-transformers/all-MiniLM-L6-v2"
  batch_size: 32
  device: "cuda"  # or "cpu"

# Chunking
chunking:
  chunk_size: 512  # tokens
  chunk_overlap: 50  # tokens
  min_chunk_size: 100  # tokens

# Retrieval
retrieval:
  top_k: 5  # number of chunks
  score_threshold: 0.3  # minimum similarity

# LLM
llm:
  model_name: "meta-llama/Llama-3.2-3B-Instruct"
  max_new_tokens: 512
  temperature: 0.7
  load_in_8bit: true
```

## Performance Considerations

### Memory Usage

| Component | Memory Usage |
|-----------|-------------|
| Embeddings (7,794 chunks) | ~12 MB |
| FAISS Index | ~15 MB |
| LLaMA 3B (8-bit) | ~3-4 GB |
| LLaMA 3B (full) | ~6-7 GB |
| Sentence Transformer | ~100 MB |

### Speed Benchmarks

| Operation | Time (CPU) | Time (GPU) |
|-----------|-----------|-----------|
| Embedding Generation | 10-15 min | 2-3 min |
| Query Encoding | 50-100 ms | 10-20 ms |
| FAISS Search | 5-10 ms | 5-10 ms |
| LLM Generation | 10-30 sec | 2-5 sec |

### Optimization Tips

1. **Use GPU**: 5-10x faster for embeddings and generation
2. **Quantization**: Reduces memory by 50-75%
3. **Batch Processing**: Process multiple queries together
4. **Index Optimization**: Use IVF for large datasets
5. **Caching**: Cache frequent queries

## API Reference

### Chatbot Class

```python
class HerHaqChatbot:
    def __init__(self, config: Dict)
    def chat(self, user_message: str) -> Dict
    def get_conversation_history(self) -> List[Dict]
    def clear_history(self)
```

### Retriever Class

```python
class Retriever:
    def __init__(self, config: Dict)
    def encode_query(self, query: str) -> np.ndarray
    def retrieve(self, query: str, top_k: int) -> List[Tuple[Dict, float]]
    def format_context(self, results: List) -> str
    def retrieve_with_context(self, query: str) -> Tuple[str, List[Dict]]
```

### VectorStore Class

```python
class VectorStore:
    def __init__(self, config: Dict)
    def build_index(self)
    def save_index(self)
    def load_index(self)
    def search(self, query_embedding: np.ndarray, top_k: int) -> List[Tuple[Dict, float]]
```

## Extending the System

### Adding New Data Sources

1. Add file to `FYP_dataset/`
2. Update `config.yaml`:
```yaml
dataset_files:
  new_category:
    - "new_file.json"
```
3. Add processing function in `data_preprocessing.py`
4. Rerun preprocessing and embedding generation

### Customizing Prompts

Edit `config.yaml`:
```yaml
prompts:
  system_prompt: |
    Your custom system prompt here...
```

### Changing Embedding Model

Update `config.yaml`:
```yaml
embedding:
  model_name: "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
```

Rerun embedding generation and vector store creation.

### Using Different LLM

Update `config.yaml`:
```yaml
llm:
  model_name: "meta-llama/Llama-3.1-8B-Instruct"
```

## Troubleshooting

### Common Issues

1. **Out of Memory**
   - Enable quantization
   - Reduce batch size
   - Use CPU for embeddings

2. **Slow Generation**
   - Use GPU
   - Reduce max_new_tokens
   - Use Ollama

3. **Poor Retrieval**
   - Adjust score_threshold
   - Increase top_k
   - Try different embedding model

4. **Irrelevant Responses**
   - Improve prompt engineering
   - Filter retrieved chunks
   - Add more context

## Security & Privacy

- All processing is local
- No external API calls (except model downloads)
- Conversation history in memory only
- No data logging by default
- HTTPS recommended for deployment

## Future Enhancements

1. **Multi-language Support**: Add Urdu language support
2. **Voice Interface**: Speech-to-text and text-to-speech
3. **Document Upload**: Allow users to upload legal documents
4. **Fine-tuning**: Fine-tune LLaMA on legal domain
5. **Feedback Loop**: Collect user feedback for improvement
6. **Mobile App**: Native mobile application
7. **Advanced RAG**: Implement hybrid search, reranking
8. **Knowledge Graph**: Add structured knowledge representation

## References

- LLaMA: https://ai.meta.com/llama/
- FAISS: https://github.com/facebookresearch/faiss
- Sentence Transformers: https://www.sbert.net/
- Streamlit: https://streamlit.io/
- RAG: https://arxiv.org/abs/2005.11401
