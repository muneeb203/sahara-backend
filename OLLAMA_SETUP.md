# 🦙 Ollama Setup Guide - Step by Step

## Why Ollama?

Ollama is the **easiest way** to run LLaMA models locally:
- ✅ No Hugging Face account needed
- ✅ No authentication required
- ✅ Automatic model management
- ✅ Lower memory usage
- ✅ Simple commands

---

## 📥 Step 1: Install Ollama (5 minutes)

### Windows Installation

1. **Open your browser** and go to:
   ```
   https://ollama.com/download
   ```

2. **Click "Download for Windows"**
   - This will download `OllamaSetup.exe` (~500MB)

3. **Run the installer**
   - Double-click `OllamaSetup.exe`
   - Click "Next" through the installation wizard
   - Accept the license agreement
   - Choose installation location (default is fine)
   - Click "Install"

4. **Wait for installation to complete**
   - This takes 2-3 minutes
   - Ollama will start automatically

5. **Verify installation**
   - Open a **NEW** PowerShell or Command Prompt window
   - Type: `ollama --version`
   - You should see something like: `ollama version 0.x.x`

**Important:** You MUST open a new terminal window after installation!

---

## 🔽 Step 2: Download LLaMA 3B Model (10-15 minutes)

Once Ollama is installed:

1. **Open PowerShell or Command Prompt**

2. **Pull the LLaMA 3B model:**
   ```bash
   ollama pull llama3:3b
   ```

3. **Wait for download to complete**
   - Model size: ~2GB
   - Time: 5-15 minutes (depending on internet speed)
   - You'll see a progress bar

4. **Verify the model is installed:**
   ```bash
   ollama list
   ```
   
   You should see:
   ```
   NAME            ID              SIZE    MODIFIED
   llama3:3b       abc123def       2.0 GB  X minutes ago
   ```

---

## ✅ Step 3: Test Ollama (1 minute)

Let's make sure Ollama is working:

```bash
ollama run llama3:3b "Hello, how are you?"
```

You should get a response from the model. Press `Ctrl+D` or type `/bye` to exit.

---

## 🚀 Step 4: Run the HerHaq Chatbot

Now you're ready to use the chatbot!

### Option A: Web Interface (Recommended)

```bash
cd herhaq_chatbot
streamlit run app.py
```

Then open: http://localhost:8501

### Option B: Command Line

```bash
cd herhaq_chatbot
python src/chatbot.py
```

---

## 🎯 Quick Test

Try asking the chatbot:
- "What are my inheritance rights as a daughter?"
- "How can I file a harassment complaint at work?"
- "Can my husband divorce me without my consent?"

---

## 🔧 Troubleshooting

### Issue: "ollama: command not found"

**Solution:**
1. Make sure Ollama is installed
2. **Close and reopen** your terminal
3. Try again

### Issue: "connection refused" or "cannot connect"

**Solution:**
1. Check if Ollama is running:
   ```bash
   ollama list
   ```
2. If not running, start it:
   ```bash
   ollama serve
   ```

### Issue: Model download is slow

**Solution:**
- This is normal for first-time download
- The model is 2GB, so it takes time
- Once downloaded, it's cached locally

### Issue: Out of memory

**Solution:**
1. Close other applications
2. Ollama uses less memory than Hugging Face
3. If still issues, try restarting your computer

---

## 📊 What Happens Behind the Scenes

When you run the chatbot:

1. **User asks a question** → "What are my inheritance rights?"
2. **Retrieval system** → Finds relevant laws/cases/ahadith
3. **Context is prepared** → Top 5 most relevant chunks
4. **Ollama generates response** → Using LLaMA 3B
5. **Response is formatted** → With source citations
6. **User sees answer** → Accurate, cited, helpful

---

## 💡 Tips

### For Faster Responses
- Keep Ollama running in the background
- First query is slower (model loading)
- Subsequent queries are faster

### For Better Answers
- Ask specific questions
- One question at a time
- Use natural language

### For Privacy
- Everything runs locally
- No data sent to external servers
- Ollama doesn't collect data

---

## 🎓 Ollama Commands Reference

```bash
# Check version
ollama --version

# List installed models
ollama list

# Pull a model
ollama pull llama3:3b

# Run a model interactively
ollama run llama3:3b

# Remove a model
ollama rm llama3:3b

# Check if Ollama is running
ollama ps

# Start Ollama server
ollama serve
```

---

## 📈 System Requirements

**Minimum:**
- 8GB RAM
- 5GB free disk space
- Windows 10 or later

**Recommended:**
- 16GB RAM
- 10GB free disk space
- SSD for faster loading

---

## 🆘 Still Having Issues?

1. **Check Ollama documentation:**
   - https://github.com/ollama/ollama

2. **Restart Ollama:**
   ```bash
   # Stop Ollama (close the app)
   # Start it again from Start Menu
   ```

3. **Reinstall Ollama:**
   - Uninstall from Control Panel
   - Download fresh installer
   - Install again

4. **Check FAQ.md** in the project folder

---

## ✅ Checklist

Before running the chatbot, make sure:

- [ ] Ollama is installed
- [ ] `ollama --version` works
- [ ] LLaMA 3B model is downloaded (`ollama list` shows it)
- [ ] Test command works (`ollama run llama3:3b "test"`)
- [ ] Config file has `use_ollama: true`
- [ ] You're in the `herhaq_chatbot` directory

---

## 🎉 You're Ready!

Once all steps are complete, run:

```bash
streamlit run app.py
```

And start asking questions about women's rights!

---

**Need help? Check FAQ.md or SETUP_GUIDE.md**

**HerHaq - Empowering Women Through Knowledge** 💜
