# HerHaq Chatbot - Frequently Asked Questions (FAQ)

## General Questions

### What is HerHaq?
HerHaq is an AI-powered chatbot that helps women understand their rights under Pakistani law and Islamic guidance. It uses Retrieval-Augmented Generation (RAG) technology to provide accurate, cited responses based on authentic legal documents, case studies, and Islamic ahadith.

### Who is this chatbot for?
- Women seeking information about their legal rights
- Legal aid organizations
- Educational institutions
- NGOs working on women's rights
- Researchers studying women's rights in Pakistan

### Is this legal advice?
No. HerHaq provides educational information only. It is not a substitute for professional legal advice. For specific legal matters, please consult a qualified lawyer.

### Is it free to use?
Yes, the chatbot is free and open-source. You can run it locally on your computer at no cost.

### What languages does it support?
Currently, HerHaq supports English only. Urdu language support is planned for future versions.

## Technical Questions

### What are the system requirements?
**Minimum:**
- Python 3.8+
- 8GB RAM
- 10GB disk space
- Internet connection (for initial setup)

**Recommended:**
- Python 3.10+
- 16GB RAM
- GPU with 6GB+ VRAM
- 20GB disk space

### Do I need a GPU?
No, but it's recommended. The chatbot works on CPU but will be slower. GPU significantly improves:
- Embedding generation speed (5-10x faster)
- Response generation speed (3-5x faster)

### How long does setup take?
- Quick setup: 15-30 minutes
- Manual setup: 20-40 minutes
- Most time is spent downloading models and generating embeddings

### What is RAG?
Retrieval-Augmented Generation (RAG) is an AI technique that:
1. Retrieves relevant information from a knowledge base
2. Provides that information as context to a language model
3. Generates accurate, grounded responses

This ensures responses are based on actual sources, not hallucinated.

### Why LLaMA 3B?
LLaMA 3B offers a good balance of:
- Performance: Good quality responses
- Size: Fits in 8GB RAM with quantization
- Speed: Fast enough for real-time chat
- Cost: Free and open-source

### Can I use a different model?
Yes! You can use:
- Larger LLaMA models (7B, 13B, 70B)
- Other models (Mistral, Falcon, etc.)
- Commercial APIs (OpenAI, Anthropic)

Edit `config.yaml` to change the model.

## Setup Questions

### Installation failed. What should I do?
1. Check Python version: `python --version` (must be 3.8+)
2. Update pip: `pip install --upgrade pip`
3. Try installing dependencies one by one
4. Check error messages for specific issues
5. See SETUP_GUIDE.md for detailed troubleshooting

### FAISS installation failed. Help!
Try these solutions:
```bash
# Solution 1: Install from conda
conda install -c conda-forge faiss-cpu

# Solution 2: Install without cache
pip install faiss-cpu --no-cache-dir

# Solution 3: Use pre-built wheel
pip install faiss-cpu==1.7.4
```

### Out of memory error. What to do?
1. Enable 8-bit quantization in `config.yaml`:
   ```yaml
   llm:
     load_in_8bit: true
   ```

2. Use Ollama instead of Hugging Face:
   ```yaml
   llm:
     use_ollama: true
   ```

3. Reduce batch size:
   ```yaml
   embedding:
     batch_size: 16
   ```

4. Use CPU for embeddings:
   ```yaml
   embedding:
     device: "cpu"
   ```

### How do I get LLaMA access?
**Option 1: Ollama (Easier)**
1. Install Ollama from https://ollama.ai
2. Run: `ollama pull llama3:3b`
3. Update config: `use_ollama: true`

**Option 2: Hugging Face**
1. Create account at https://huggingface.co
2. Accept license at https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct
3. Login: `huggingface-cli login`

### Dataset not found error?
Ensure FYP_dataset is in the parent directory:
```
parent_folder/
├── FYP_dataset/
│   ├── case_studies_dataset.json
│   ├── dataset_penal_code.json
│   └── ...
└── herhaq_chatbot/
    ├── src/
    └── ...
```

Or update the path in `config.yaml`:
```yaml
data:
  source_dir: "/path/to/FYP_dataset"
```

## Usage Questions

### How do I start the chatbot?
**Web Interface (Recommended):**
```bash
streamlit run app.py
```
Then open http://localhost:8501 in your browser.

**Command Line:**
```bash
python src/chatbot.py
```

### How do I ask a question?
Simply type your question in natural language. Examples:
- "What are my inheritance rights?"
- "Can my husband divorce me without my consent?"
- "How do I file a harassment complaint?"

### Why are responses slow?
Response time depends on:
- Hardware (CPU vs GPU)
- Model size
- Query complexity

Typical times:
- With GPU: 2-5 seconds
- With CPU: 10-30 seconds

To speed up:
- Use GPU
- Use Ollama
- Reduce `max_new_tokens` in config

### Can I see the sources?
Yes! Every response includes source citations. In the web interface, click "View Sources" to see:
- Source name
- Reference (section/hadith number)
- Relevance score

### How accurate are the responses?
Accuracy depends on:
- Quality of retrieved context
- LLM's understanding
- Query clarity

The system:
- ✅ Always cites sources
- ✅ Based on authentic documents
- ✅ Includes disclaimers
- ❌ Not 100% perfect
- ❌ Should be verified for critical matters

### What if I don't like a response?
- Try rephrasing your question
- Ask for more specific information
- Check the sources provided
- Consult a legal professional for verification

## Data Questions

### What data does the chatbot use?
1. **Pakistani Laws** (274 items):
   - Muslim Family Laws Ordinance
   - Harassment Protection Act
   - Women's Rights Acts
   - Penal Code provisions

2. **Case Studies** (15 items):
   - Real legal cases
   - Court decisions
   - Precedents

3. **Islamic Ahadith** (7,610 items):
   - Sahih Muslim collection
   - Filtered for women's rights topics

### How current is the data?
The dataset includes laws and cases up to 2024. However:
- Laws may have been amended
- New cases may exist
- Always verify with current sources

### Can I add more data?
Yes! To add new data:
1. Add JSON files to FYP_dataset
2. Update `config.yaml`
3. Rerun preprocessing:
   ```bash
   python src/data_preprocessing.py
   python src/embedding_generator.py
   python src/vector_store.py
   ```

### Is my data private?
Yes! Everything runs locally:
- No data sent to external servers
- No logging of conversations
- No tracking or analytics
- Conversation history in memory only

## Customization Questions

### Can I change the chatbot's personality?
Yes! Edit the system prompt in `config.yaml`:
```yaml
prompts:
  system_prompt: |
    Your custom instructions here...
```

### Can I adjust retrieval settings?
Yes! In `config.yaml`:
```yaml
retrieval:
  top_k: 5              # Number of chunks to retrieve
  score_threshold: 0.3  # Minimum similarity score
```

### Can I use a different embedding model?
Yes! Update `config.yaml`:
```yaml
embedding:
  model_name: "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
```
Then regenerate embeddings.

### Can I change the UI?
Yes! The web interface is in `app.py`. You can:
- Modify colors and styling
- Add new features
- Change layout
- Add authentication

## Deployment Questions

### Can I deploy this online?
Yes! See DEPLOYMENT.md for options:
- Streamlit Cloud (easiest)
- Docker
- AWS/Azure/GCP
- Heroku
- Your own server

### How much does deployment cost?
Depends on platform:
- **Local**: Free
- **Streamlit Cloud**: Free tier available
- **AWS**: ~$60-95/month
- **Heroku**: Free tier (limited)

### Can multiple users use it simultaneously?
Yes, but consider:
- Each user needs resources
- May need load balancing
- Consider cloud deployment for scale

### How do I secure the deployment?
1. Enable HTTPS
2. Add authentication
3. Implement rate limiting
4. Use environment variables for secrets
5. Regular security updates

See DEPLOYMENT.md for details.

## Troubleshooting Questions

### Chatbot gives irrelevant answers?
Try:
1. Rephrase your question more clearly
2. Be more specific
3. Check retrieved sources
4. Adjust `score_threshold` in config
5. Increase `top_k` for more context

### "Module not found" error?
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Or install specific module
pip install <module-name>
```

### Streamlit won't start?
```bash
# Check if port is in use
netstat -an | grep 8501

# Use different port
streamlit run app.py --server.port 8502

# Check Streamlit installation
pip install --upgrade streamlit
```

### Model download is stuck?
1. Check internet connection
2. Try different network
3. Use VPN if blocked
4. Download manually and specify path
5. Use Ollama instead

### Response is cut off?
Increase `max_new_tokens` in `config.yaml`:
```yaml
llm:
  max_new_tokens: 1024  # Increase from 512
```

## Performance Questions

### How can I make it faster?
1. Use GPU
2. Use Ollama
3. Enable quantization
4. Reduce `max_new_tokens`
5. Use smaller embedding model
6. Implement caching

### How much disk space is needed?
- Embeddings: ~50MB
- LLaMA 3B model: 3-7GB
- Dependencies: ~2GB
- Logs and cache: ~100MB
- **Total**: ~5-10GB

### Can I run this on a laptop?
Yes! Requirements:
- Modern laptop (2020+)
- 8GB+ RAM
- 10GB free disk space
- Works without GPU (slower)

### How many queries can it handle?
Depends on hardware:
- Single user: No limit
- Multiple users: 5-10 concurrent (typical laptop)
- Production: 50-100+ (with proper infrastructure)

## Support Questions

### Where can I get help?
1. Read documentation (README, SETUP_GUIDE, etc.)
2. Check this FAQ
3. Search GitHub issues
4. Create new issue on GitHub
5. Contact maintainers

### How do I report a bug?
1. Check if it's already reported
2. Create GitHub issue with:
   - Description of problem
   - Steps to reproduce
   - Error messages
   - System information
   - Screenshots if applicable

### How can I contribute?
1. Report bugs
2. Suggest features
3. Improve documentation
4. Add data sources
5. Submit pull requests
6. Help other users

### Is there a community?
Check:
- GitHub Discussions
- Issue tracker
- Project website
- Social media

## Legal and Ethical Questions

### Is this legal to use?
Yes, for educational and informational purposes. However:
- Not a substitute for legal advice
- Users responsible for their actions
- Verify information with professionals

### What about data privacy?
- All processing is local
- No data collection
- No external API calls (except model downloads)
- No tracking
- User privacy protected

### Can I use this commercially?
Check the license. Generally:
- Educational use: ✅ Yes
- Non-profit use: ✅ Yes
- Commercial use: Check license terms
- Modifications: Check license terms

### What are the limitations?
1. **Not legal advice**: Educational only
2. **May have errors**: Always verify
3. **Limited scope**: Pakistani law and Islamic guidance
4. **Language**: English only currently
5. **Updates**: Manual updates required
6. **Model limitations**: LLaMA 3B has constraints

## Future Questions

### What's coming next?
Planned features:
- Urdu language support
- Voice interface
- Mobile apps
- Fine-tuned model
- Real-time updates
- Community features

### Can I request features?
Yes! Create a GitHub issue with:
- Feature description
- Use case
- Why it's important
- Proposed implementation (optional)

### How often is it updated?
- Bug fixes: As needed
- Security updates: Immediately
- Feature updates: Quarterly
- Data updates: As available
- Model updates: When beneficial

### Will it always be free?
The open-source version will remain free. Potential future:
- Hosted service (may have costs)
- Premium features (optional)
- Enterprise version (for organizations)
- Core functionality: Always free

## Contact

### Need more help?
- 📧 Email: [contact email]
- 💬 GitHub: [repository link]
- 📖 Docs: See documentation folder
- 🐛 Issues: GitHub issue tracker

---

**Last Updated**: December 2024  
**Version**: 1.0.0

*Don't see your question? Create an issue on GitHub or contact us!*
