# HerHaq RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot using LLaMA 3B to assist women by providing guidance based on Pakistani laws, case studies, and Islamic ahadith.

## 🌟 Overview

HerHaq empowers women with knowledge about their rights through:
- **Accurate Information**: Based on authentic Pakistani laws and Islamic sources
- **Source Citations**: Every response includes verifiable references
- **Empathetic Design**: Supportive, non-judgmental, and privacy-focused
- **Practical Guidance**: Step-by-step instructions and actionable advice
- **Free & Open Source**: Run locally with complete privacy

## 🚀 Quick Start

```bash
# 1. Navigate to project
cd herhaq_chatbot

# 2. Run automated setup (15-30 minutes)
python quick_start.py

# 3. Start the chatbot
streamlit run app.py
```

**That's it!** Open http://localhost:8501 in your browser.

For detailed instructions, see [GETTING_STARTED.md](GETTING_STARTED.md)

## 📋 Project Structure

```
herhaq_chatbot/
├── src/                       # Source code
│   ├── data_preprocessing.py  # Dataset cleaning and chunking
│   ├── embedding_generator.py # Vector embedding generation
│   ├── vector_store.py        # FAISS vector database
│   ├── retriever.py           # Semantic search
│   ├── llm_interface.py       # LLaMA 3B integration
│   ├── chatbot.py             # Main RAG pipeline
│   └── utils.py               # Helper functions
├── data/processed/            # Processed dataset chunks
├── embeddings/                # Vector embeddings & FAISS index
├── logs/                      # Application logs
├── app.py                     # Streamlit web interface
├── config.yaml                # Configuration file
├── requirements.txt           # Python dependencies
├── quick_start.py             # Automated setup script
├── test_pipeline.py           # Testing script
└── [Documentation files]      # See below
```

## ✨ Features

### Core Capabilities
- 🔍 **Semantic Search**: FAISS-based vector retrieval for accurate context
- 🤖 **LLaMA 3B Generation**: Context-aware, empathetic responses
- 📚 **Multi-source Knowledge**: 7,899 items from laws, cases, and ahadith
- 📖 **Source Citations**: Every response includes verifiable references
- 💬 **Natural Conversation**: Easy-to-use chat interface
- 🔒 **Privacy First**: All processing done locally

### Knowledge Base
- **274** Pakistani legal provisions
- **15** Case studies with outcomes
- **7,610** Islamic ahadith on women's rights

### Topics Covered
- Inheritance & Property Rights
- Marriage & Divorce
- Workplace Harassment
- Legal Protections
- Islamic Guidance
- Family Law

## 📖 Documentation

| Document | Description |
|----------|-------------|
| **[GETTING_STARTED.md](GETTING_STARTED.md)** | Quick start guide - **Read this first!** |
| **[SETUP_GUIDE.md](SETUP_GUIDE.md)** | Detailed setup instructions |
| **[FAQ.md](FAQ.md)** | Frequently asked questions |
| **[SAMPLE_INTERACTIONS.md](SAMPLE_INTERACTIONS.md)** | Example conversations |
| **[DOCUMENTATION.md](DOCUMENTATION.md)** | Technical documentation |
| **[DEPLOYMENT.md](DEPLOYMENT.md)** | Production deployment guide |
| **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | Complete project overview |
| **[CHECKLIST.md](CHECKLIST.md)** | Setup verification checklist |

## 💻 Installation

### Automated Setup (Recommended)
```bash
python quick_start.py
```

### Manual Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Process dataset
python src/data_preprocessing.py

# 3. Generate embeddings
python src/embedding_generator.py

# 4. Build vector store
python src/vector_store.py

# 5. Test pipeline
python test_pipeline.py
```

## 🎯 Usage

### Web Interface (Recommended)
```bash
streamlit run app.py
```
Open http://localhost:8501

### API Server (for frontend integration)
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```
Health check:
```bash
curl http://localhost:8000/health
```
Chat request:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"What are my inheritance rights?\",\"session_id\":\"user-1\"}"
```

### Command Line
```bash
python src/chatbot.py
```

### Example Queries
- "What are my inheritance rights as a daughter?"
- "How can I file a harassment complaint at work?"
- "Can my husband divorce me without my consent?"
- "What does Islam say about women's property rights?"

## 🔧 Configuration

### LLM Setup

**Option 1: Ollama (Recommended)**
```bash
# Install from https://ollama.ai
ollama pull llama3:3b

# Update config.yaml
llm:
  use_ollama: true
```

**Option 2: Hugging Face**
```bash
huggingface-cli login
# Accept license at: https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct
```

### System Requirements

**Minimum:**
- Python 3.8+
- 8GB RAM
- 10GB disk space

**Recommended:**
- Python 3.10+
- 16GB RAM
- GPU with 6GB+ VRAM

## 🧪 Testing

```bash
# Run comprehensive tests
python test_pipeline.py

# Test retrieval only
python src/retriever.py

# Test LLM interface
python src/llm_interface.py
```

## 🛠️ Technical Stack

- **Language Model**: LLaMA 3.2-3B-Instruct
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2 (384-dim)
- **Vector Store**: FAISS (IndexFlatL2)
- **Web Framework**: Streamlit
- **Deep Learning**: PyTorch, Transformers
- **Data Processing**: Pandas, NumPy

## 📊 Performance

- **Query Encoding**: 10-50ms
- **Vector Search**: 5-10ms
- **LLM Generation**: 2-30s (hardware dependent)
- **Total Response**: 3-35s

## 🚀 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Local server setup
- Cloud deployment (AWS, Azure, GCP)
- Docker containerization
- Streamlit Cloud deployment
- Production best practices

### Render API Deployment
This repository now includes `render.yaml` for one-click Render deployment as an API service.

Start command on Render:
```bash
uvicorn api:app --host 0.0.0.0 --port $PORT
```

Recommended Render environment variables:
- `USE_OLLAMA=false`
- `HF_API_TOKEN=<your_huggingface_token>`
- `HF_API_MODEL=mistralai/Mistral-7B-Instruct-v0.3`
- `CORS_ORIGINS=https://your-frontend-domain.com`

After deploy, call:
- `GET /health`
- `POST /chat`

## 🤝 Contributing

We welcome contributions!

1. Report bugs via GitHub Issues
2. Suggest features
3. Improve documentation
4. Add data sources
5. Submit pull requests

See [CHECKLIST.md](CHECKLIST.md) for development guidelines.

## 📞 Support

- 📖 **Documentation**: See docs above
- 🐛 **Issues**: GitHub Issues
- 💬 **Discussions**: GitHub Discussions
- 📧 **Contact**: [Your contact info]

## ⚠️ Important Disclaimers

- **Not Legal Advice**: This chatbot provides educational information only
- **Verify Information**: Always consult qualified legal professionals
- **Privacy**: All processing is local; no data is sent externally
- **Accuracy**: While based on authentic sources, responses should be verified

## 🆘 Emergency Contacts

- **Emergency**: 1122
- **Women Helpline**: 1099
- **Rozan (Psychological Support)**: 0800-22222
- **Police**: 15

## 📜 License

This project is for educational and social welfare purposes. See LICENSE file for details.

## 🙏 Acknowledgments

- **Data Sources**: FYP_dataset (Pakistani laws and case studies)
- **Technologies**: Meta AI (LLaMA), Hugging Face, Facebook Research (FAISS)
- **Community**: All contributors and supporters

## 📈 Project Status

- ✅ **Status**: Production Ready
- 📅 **Version**: 1.0.0
- 🔄 **Last Updated**: December 2024
- 🎯 **Next**: User testing and feedback collection

---

**HerHaq - Empowering Women Through Knowledge** 💜

*For detailed information, start with [GETTING_STARTED.md](GETTING_STARTED.md)*
