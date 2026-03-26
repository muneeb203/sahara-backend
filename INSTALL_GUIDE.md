# HerHaq Chatbot - Installation Guide

## Quick Fix for Current Issues

If you're getting import errors, follow these steps:

### Step 1: Install Essential Dependencies

```bash
# Navigate to project directory
cd herhaq_chatbot

# Install essential packages one by one to avoid conflicts
pip install torch>=2.0.0
pip install transformers>=4.35.0
pip install sentence-transformers>=2.2.2
pip install faiss-cpu>=1.7.4
pip install huggingface-hub>=0.19.0
pip install accelerate>=0.25.0
pip install bitsandbytes>=0.41.0
pip install pandas>=2.0.0
pip install numpy>=1.24.0
pip install PyYAML>=6.0
pip install streamlit>=1.29.0
pip install tqdm>=4.66.0
pip install requests>=2.31.0
```

### Step 2: Install Ollama (Recommended for easier setup)

```bash
pip install ollama>=0.1.7
```

### Step 3: Test Installation

```bash
# Test data preprocessing
python src/data_preprocessing.py

# Test embedding generation
python src/embedding_generator.py

# Test vector store
python src/vector_store.py

# Test full pipeline
python test_pipeline.py
```

### Step 4: Run the Chatbot

```bash
# Web interface (recommended)
streamlit run app.py

# Or command line interface
python src/chatbot.py
```

## Alternative: Use Minimal Requirements

```bash
# Install from minimal requirements file
pip install -r requirements_minimal.txt
```

## Troubleshooting

### Issue: "No module named 'yaml'"
```bash
pip install PyYAML>=6.0
```

### Issue: "No module named 'torch'"
```bash
pip install torch>=2.0.0
```

### Issue: "No module named 'faiss'"
```bash
pip install faiss-cpu>=1.7.4
```

### Issue: Out of Memory
```bash
# Use CPU-only versions
pip uninstall torch
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Issue: GPU Support
```bash
# For NVIDIA GPU support
pip uninstall faiss-cpu
pip install faiss-gpu>=1.7.4
```

## System Requirements

- **Python**: 3.8 or higher
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 10GB free space
- **GPU**: Optional but recommended (6GB+ VRAM)

## Next Steps

1. Configure LLaMA model (see README.md)
2. Run the quick start script: `python quick_start.py`
3. Start using the chatbot!