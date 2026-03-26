# Getting Started with HerHaq Chatbot

Welcome! This guide will help you get the HerHaq chatbot up and running in just a few steps.

## 🚀 Quick Start (5 Minutes)

### Step 1: Check Prerequisites

```bash
# Check Python version (need 3.8+)
python --version

# Verify dataset exists
ls ../FYP_dataset
```

### Step 2: Install and Setup

```bash
# Navigate to project
cd herhaq_chatbot

# Run automated setup
python quick_start.py
```

This will:
- Install all dependencies
- Process the dataset
- Generate embeddings
- Build the vector store
- Run tests

**Time**: 15-30 minutes

### Step 3: Configure LLM

Choose one option:

**Option A: Ollama (Recommended - Easier)**
```bash
# 1. Install Ollama from https://ollama.ai
# 2. Pull model
ollama pull llama3:3b

# 3. Update config.yaml
# Set: llm.use_ollama: true
```

**Option B: Hugging Face**
```bash
# 1. Login
huggingface-cli login

# 2. Accept license at:
# https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct
```

### Step 4: Run the Chatbot

```bash
# Start web interface
streamlit run app.py
```

Open http://localhost:8501 in your browser.

**That's it! You're ready to go! 🎉**

---

## 📚 What to Read Next

### For First-Time Users
1. **README.md** - Project overview
2. **SAMPLE_INTERACTIONS.md** - See example conversations
3. **FAQ.md** - Common questions answered

### For Setup Issues
1. **SETUP_GUIDE.md** - Detailed setup instructions
2. **FAQ.md** - Troubleshooting section
3. **CHECKLIST.md** - Verify your setup

### For Developers
1. **DOCUMENTATION.md** - Technical details
2. **PROJECT_SUMMARY.md** - Architecture overview
3. **DEPLOYMENT.md** - Production deployment

---

## 🎯 Try These First Questions

Once the chatbot is running, try asking:

1. **Inheritance Rights**
   > "What are my inheritance rights as a daughter?"

2. **Workplace Harassment**
   > "How can I file a harassment complaint at work?"

3. **Marriage Rights**
   > "Can my husband marry another woman without my permission?"

4. **Divorce**
   > "What happens if my husband says talaq three times?"

5. **Property Rights**
   > "Can I buy property in my own name?"

---

## 🔧 Common Issues and Quick Fixes

### Issue: "Module not found"
```bash
pip install --force-reinstall -r requirements.txt
```

### Issue: "Out of memory"
Edit `config.yaml`:
```yaml
llm:
  load_in_8bit: true
```

### Issue: "Dataset not found"
Verify path in `config.yaml`:
```yaml
data:
  source_dir: "../FYP_dataset"
```

### Issue: "Slow responses"
Use Ollama instead:
```yaml
llm:
  use_ollama: true
```

---

## 📖 Documentation Overview

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **README.md** | Project overview | First |
| **GETTING_STARTED.md** | Quick start guide | First |
| **SETUP_GUIDE.md** | Detailed setup | If issues occur |
| **FAQ.md** | Common questions | When stuck |
| **DOCUMENTATION.md** | Technical details | For developers |
| **SAMPLE_INTERACTIONS.md** | Example usage | To understand capabilities |
| **DEPLOYMENT.md** | Production setup | For deployment |
| **PROJECT_SUMMARY.md** | Complete overview | For understanding architecture |
| **CHECKLIST.md** | Setup verification | To verify setup |

---

## 🎓 Learning Path

### Beginner Path
1. Read README.md
2. Run quick_start.py
3. Try sample questions
4. Read SAMPLE_INTERACTIONS.md
5. Explore FAQ.md

### Developer Path
1. Read PROJECT_SUMMARY.md
2. Study DOCUMENTATION.md
3. Review source code
4. Run test_pipeline.py
5. Make modifications

### Deployment Path
1. Complete beginner path
2. Read DEPLOYMENT.md
3. Choose deployment option
4. Set up monitoring
5. Go live

---

## 💡 Tips for Best Results

### Asking Questions
- ✅ Be specific and clear
- ✅ Use natural language
- ✅ Ask one question at a time
- ❌ Don't use abbreviations
- ❌ Don't ask multiple questions together

### Understanding Responses
- Always check the sources cited
- Read the full response
- Note the disclaimer
- Verify critical information with a lawyer

### Using the Interface
- Use example questions to get started
- Expand sources to see references
- Clear history for privacy
- Check emergency contacts if needed

---

## 🆘 Getting Help

### Self-Help Resources
1. **FAQ.md** - Most common issues covered
2. **SETUP_GUIDE.md** - Detailed troubleshooting
3. **Documentation** - Technical details
4. **Error logs** - Check `logs/chatbot.log`

### Community Help
1. **GitHub Issues** - Report bugs
2. **GitHub Discussions** - Ask questions
3. **Documentation** - Comprehensive guides

### Professional Help
For legal matters, always consult:
- Qualified lawyers
- Legal aid organizations
- Women's rights NGOs

---

## 🎯 Success Checklist

After setup, verify:

- [ ] Web interface opens
- [ ] Can type and send messages
- [ ] Chatbot responds
- [ ] Sources are displayed
- [ ] Example questions work
- [ ] No error messages

If all checked, you're good to go! ✅

---

## 🌟 What Makes HerHaq Special?

### 1. Accurate Information
- Based on real Pakistani laws
- Authentic Islamic ahadith
- Verified case studies
- Always cites sources

### 2. Empathetic Design
- Supportive tone
- Sensitive to personal situations
- Non-judgmental
- Privacy-focused

### 3. Practical Guidance
- Step-by-step instructions
- Actionable advice
- Clear explanations
- Emergency contacts

### 4. Accessible
- Easy to use
- No technical knowledge needed
- Free and open-source
- Runs locally

---

## 📊 What to Expect

### Response Time
- With GPU: 2-5 seconds
- With CPU: 10-30 seconds
- First query may be slower (model loading)

### Response Quality
- Accurate and cited
- Based on authentic sources
- Includes disclaimers
- May need verification for critical matters

### Coverage
- Pakistani laws
- Islamic guidance
- Case studies
- Women's rights topics

---

## 🔄 Next Steps After Setup

### Immediate
1. Try the example questions
2. Explore different topics
3. Check the sources
4. Read sample interactions

### Short-term
1. Customize the system prompt
2. Adjust retrieval settings
3. Add more data if needed
4. Share with others

### Long-term
1. Deploy for wider access
2. Collect user feedback
3. Contribute improvements
4. Help others set up

---

## 🎉 You're Ready!

You now have a powerful AI assistant to help understand women's rights under Pakistani law and Islamic guidance.

**Remember:**
- This is educational information
- Always verify critical matters with professionals
- Your privacy is protected
- Help is available if needed

**Emergency Contacts:**
- Emergency: 1122
- Women Helpline: 1099
- Rozan: 0800-22222
- Police: 15

---

## 📞 Need Help?

- 📖 Read the documentation
- 🔍 Check FAQ.md
- 🐛 Report issues on GitHub
- 💬 Ask in discussions
- 📧 Contact maintainers

---

**Welcome to HerHaq! Empowering women through knowledge. 💜**

*Last Updated: December 2024*
*Version: 1.0.0*
