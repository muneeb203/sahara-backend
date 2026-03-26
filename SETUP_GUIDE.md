# HerHaq Chatbot - Complete Setup Guide

This guide will walk you through setting up and running the HerHaq RAG-based chatbot.

## Prerequisites

- Python 3.8 or higher
- 8GB+ RAM (16GB recommended for LLaMA 3B)
- GPU with 6GB+ VRAM (optional but recommended)
- Internet connection for downloading models

## Step-by-Step Setup

### 1. Create Virtual Environment

```bash
# Navigate to the project directory
cd herhaq_chatbot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note**: If you encounter issues with `faiss-cpu`, try:
```bash
pip install faiss-cpu --no-cache-dir
```

For GPU support with FAISS:
```bash
pip uninstall faiss-cpu
pip install faiss-gpu
```

### 3. Configure the System

Edit `config.yaml` to match your setup:

```yaml
# For CPU-only systems
embedding:
  device: "cpu"

llm:
  load_in_8bit: true  # Reduces memory usage
  use_ollama: false   # Set to true if using Ollama
```

### 4. Prepare the Dataset

The chatbot expects the FYP_dataset folder to be in the parent directory. Verify the path in `config.yaml`:

```yaml
data:
  source_dir: "../FYP_dataset"
```

### 5. Run Data Preprocessing

This step cleans and chunks the dataset:

```bash
python src/data_preprocessing.py
```

**Expected output:**
- `data/processed/processed_chunks.json` - All text chunks
- `data/processed/processing_stats.json` - Statistics

**Time**: 2-5 minutes

### 6. Generate Embeddings

This creates vector embeddings for semantic search:

```bash
python src/embedding_generator.py
```

**Expected output:**
- `embeddings/embeddings.npy` - Vector embeddings
- `embeddings/chunks_metadata.json` - Chunk metadata
- `embeddings/embedding_info.json` - Embedding information

**Time**: 5-15 minutes (depending on hardware)

### 7. Build Vector Index

Create the FAISS index for fast retrieval:

```bash
python src/vector_store.py
```

**Expected output:**
- `embeddings/faiss_index.bin` - FAISS index file

**Time**: 1-2 minutes

### 8. Test the Pipeline

Verify everything works:

```bash
python test_pipeline.py
```

This will test:
- Dataset statistics
- Retrieval functionality
- (Optional) Full pipeline with LLM

## Running the Chatbot

### Option 1: Command Line Interface

```bash
python src/chatbot.py
```

Interactive CLI where you can ask questions directly.

### Option 2: Web Interface (Recommended)

```bash
streamlit run app.py
```

Opens a web browser with a user-friendly interface.

**Default URL**: http://localhost:8501

## LLaMA Model Setup

### Option A: Using Hugging Face (Default)

The chatbot will automatically download LLaMA 3.2-3B-Instruct from Hugging Face.

**Requirements:**
- Hugging Face account
- Accept the LLaMA license at: https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct

**Login to Hugging Face:**
```bash
pip install huggingface-hub
huggingface-cli login
```

### Option B: Using Ollama (Easier, Recommended for Beginners)

1. Install Ollama from: https://ollama.ai

2. Pull LLaMA 3B:
```bash
ollama pull llama3:3b
```

3. Update `config.yaml`:
```yaml
llm:
  use_ollama: true
  ollama_base_url: "http://localhost:11434"
```

4. Start Ollama (if not running):
```bash
ollama serve
```

## Troubleshooting

### Issue: Out of Memory

**Solution 1**: Use 8-bit quantization
```yaml
llm:
  load_in_8bit: true
```

**Solution 2**: Use Ollama instead of Hugging Face

**Solution 3**: Reduce batch size
```yaml
embedding:
  batch_size: 16  # Reduce from 32
```

### Issue: CUDA Out of Memory

**Solution**: Use CPU for embeddings
```yaml
embedding:
  device: "cpu"
```

### Issue: Slow Generation

**Solution 1**: Use GPU if available

**Solution 2**: Reduce max tokens
```yaml
llm:
  max_new_tokens: 256  # Reduce from 512
```

### Issue: Import Errors

**Solution**: Reinstall dependencies
```bash
pip install --force-reinstall -r requirements.txt
```

### Issue: FAISS Installation Failed

**Solution**: Install from conda
```bash
conda install -c conda-forge faiss-cpu
```

## Performance Optimization

### For Low-End Systems (8GB RAM, No GPU)

```yaml
embedding:
  device: "cpu"
  batch_size: 16

llm:
  use_ollama: true
  load_in_8bit: true
  max_new_tokens: 256
```

### For High-End Systems (16GB+ RAM, GPU)

```yaml
embedding:
  device: "cuda"
  batch_size: 64

llm:
  use_ollama: false
  load_in_8bit: false
  max_new_tokens: 512
```

## Testing the Chatbot

### Sample Questions to Try

1. **Inheritance Rights**
   - "What are my inheritance rights as a daughter?"
   - "How much property do I inherit from my father?"

2. **Marriage & Divorce**
   - "Can my husband divorce me without my consent?"
   - "What are my rights if my husband wants a second wife?"

3. **Workplace Harassment**
   - "How do I file a harassment complaint at work?"
   - "What are the penalties for workplace harassment?"

4. **Islamic Guidance**
   - "What does Islam say about women's property rights?"
   - "Are women allowed to work in Islam?"

## Directory Structure After Setup

```
herhaq_chatbot/
├── data/
│   └── processed/
│       ├── processed_chunks.json
│       └── processing_stats.json
├── embeddings/
│   ├── embeddings.npy
│   ├── chunks_metadata.json
│   ├── embedding_info.json
│   └── faiss_index.bin
├── logs/
│   └── chatbot.log
├── src/
│   └── [source files]
├── venv/
│   └── [virtual environment]
├── app.py
├── config.yaml
├── requirements.txt
└── README.md
```

## Next Steps

1. **Customize Prompts**: Edit `config.yaml` to adjust the system prompt
2. **Add More Data**: Include additional legal documents or case studies
3. **Fine-tune Retrieval**: Adjust `top_k` and `score_threshold` in config
4. **Deploy**: Consider deploying on a server for wider access

## Support & Resources

- **LLaMA Documentation**: https://huggingface.co/meta-llama
- **FAISS Documentation**: https://github.com/facebookresearch/faiss
- **Streamlit Documentation**: https://docs.streamlit.io
- **Sentence Transformers**: https://www.sbert.net

## Security & Privacy

- All processing is done locally
- No data is sent to external servers (except model downloads)
- Conversation history is stored in memory only
- Clear history regularly for privacy

## License & Disclaimer

This chatbot is for educational purposes only. It does not provide legal advice. Users should consult qualified legal professionals for specific legal matters.
