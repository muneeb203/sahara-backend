# HerHaq Chatbot - Deployment Guide

This guide covers deploying the HerHaq chatbot for production use.

## Deployment Options

### Option 1: Local Server (Recommended for Testing)

**Pros:**
- Full control
- No cloud costs
- Data privacy

**Cons:**
- Limited accessibility
- Requires maintenance
- Hardware dependent

**Setup:**
```bash
# Run on local network
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Access from other devices on the same network: `http://<your-ip>:8501`

---

### Option 2: Cloud Deployment (Streamlit Cloud)

**Pros:**
- Easy deployment
- Free tier available
- Automatic HTTPS

**Cons:**
- Resource limitations
- Public repository required
- Limited to Streamlit

**Steps:**

1. **Prepare Repository**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo>
git push -u origin main
```

2. **Create requirements.txt for Cloud**
```txt
streamlit>=1.29.0
torch>=2.0.0
transformers>=4.35.0
sentence-transformers>=2.2.2
faiss-cpu>=1.7.4
pandas>=2.0.0
numpy>=1.24.0
pyyaml>=6.0
```

3. **Deploy on Streamlit Cloud**
- Go to https://streamlit.io/cloud
- Connect your GitHub repository
- Select `app.py` as the main file
- Deploy

**Note:** LLaMA 3B may be too large for Streamlit Cloud's free tier. Consider using Ollama or a smaller model.

---

### Option 3: Docker Deployment

**Pros:**
- Consistent environment
- Easy scaling
- Portable

**Cons:**
- Requires Docker knowledge
- Resource intensive

**Dockerfile:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Run preprocessing on first start
RUN python src/data_preprocessing.py && \
    python src/embedding_generator.py && \
    python src/vector_store.py

# Start application
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

**Build and Run:**
```bash
# Build image
docker build -t herhaq-chatbot .

# Run container
docker run -p 8501:8501 herhaq-chatbot
```

---

### Option 4: AWS Deployment

**Pros:**
- Scalable
- Professional
- Reliable

**Cons:**
- Costs money
- Complex setup
- Requires AWS knowledge

**Architecture:**
```
User → CloudFront → ALB → ECS (Fargate) → Container
                                ↓
                              S3 (embeddings)
```

**Steps:**

1. **Prepare Container**
```bash
# Build and tag
docker build -t herhaq-chatbot .
docker tag herhaq-chatbot:latest <aws-account-id>.dkr.ecr.<region>.amazonaws.com/herhaq-chatbot:latest

# Push to ECR
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws-account-id>.dkr.ecr.<region>.amazonaws.com
docker push <aws-account-id>.dkr.ecr.<region>.amazonaws.com/herhaq-chatbot:latest
```

2. **Create ECS Task Definition**
```json
{
  "family": "herhaq-chatbot",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "2048",
  "memory": "8192",
  "containerDefinitions": [
    {
      "name": "herhaq-chatbot",
      "image": "<ecr-image-uri>",
      "portMappings": [
        {
          "containerPort": 8501,
          "protocol": "tcp"
        }
      ]
    }
  ]
}
```

3. **Create ECS Service**
```bash
aws ecs create-service \
  --cluster herhaq-cluster \
  --service-name herhaq-service \
  --task-definition herhaq-chatbot \
  --desired-count 1 \
  --launch-type FARGATE
```

---

### Option 5: Heroku Deployment

**Pros:**
- Simple deployment
- Free tier available
- Good for prototypes

**Cons:**
- Resource limitations
- Sleeps after inactivity
- Limited to 512MB RAM on free tier

**Files Needed:**

**Procfile:**
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**runtime.txt:**
```
python-3.10.12
```

**Deploy:**
```bash
heroku login
heroku create herhaq-chatbot
git push heroku main
```

**Note:** Free tier won't support LLaMA 3B. Use Ollama API or smaller model.

---

## Production Considerations

### 1. Security

**HTTPS:**
```bash
# For local deployment with SSL
streamlit run app.py --server.sslCertFile cert.pem --server.sslKeyFile key.pem
```

**Authentication:**
```python
# Add to app.py
import streamlit as st

def check_password():
    def password_entered():
        if st.session_state["password"] == "your_secure_password":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        return True

if not check_password():
    st.stop()
```

**Rate Limiting:**
```python
# Add to chatbot.py
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_requests=10, time_window=60):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = {}
    
    def is_allowed(self, user_id):
        now = datetime.now()
        if user_id not in self.requests:
            self.requests[user_id] = []
        
        # Remove old requests
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id]
            if now - req_time < timedelta(seconds=self.time_window)
        ]
        
        if len(self.requests[user_id]) < self.max_requests:
            self.requests[user_id].append(now)
            return True
        return False
```

### 2. Performance Optimization

**Caching:**
```python
# Add to app.py
@st.cache_data(ttl=3600)
def get_cached_response(query):
    return chatbot.chat(query)
```

**Load Balancing:**
```nginx
# nginx.conf
upstream herhaq_backend {
    server 127.0.0.1:8501;
    server 127.0.0.1:8502;
    server 127.0.0.1:8503;
}

server {
    listen 80;
    server_name herhaq.example.com;
    
    location / {
        proxy_pass http://herhaq_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 3. Monitoring

**Logging:**
```python
# Enhanced logging
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'logs/chatbot.log',
    maxBytes=10485760,  # 10MB
    backupCount=5
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[handler]
)
```

**Metrics:**
```python
# Add to chatbot.py
class ChatbotMetrics:
    def __init__(self):
        self.total_queries = 0
        self.successful_responses = 0
        self.failed_responses = 0
        self.average_response_time = 0
    
    def log_query(self, success, response_time):
        self.total_queries += 1
        if success:
            self.successful_responses += 1
        else:
            self.failed_responses += 1
        
        # Update average
        self.average_response_time = (
            (self.average_response_time * (self.total_queries - 1) + response_time)
            / self.total_queries
        )
```

### 4. Backup and Recovery

**Backup Script:**
```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups/$DATE"

mkdir -p $BACKUP_DIR

# Backup embeddings
cp -r embeddings $BACKUP_DIR/

# Backup processed data
cp -r data/processed $BACKUP_DIR/

# Backup config
cp config.yaml $BACKUP_DIR/

# Backup logs
cp -r logs $BACKUP_DIR/

echo "Backup completed: $BACKUP_DIR"
```

### 5. Scaling

**Horizontal Scaling:**
- Deploy multiple instances behind a load balancer
- Use shared storage for embeddings (S3, NFS)
- Implement session affinity if needed

**Vertical Scaling:**
- Increase CPU/RAM for faster processing
- Use GPU instances for better performance
- Optimize batch sizes

### 6. Cost Optimization

**AWS Cost Estimates:**
- ECS Fargate (2 vCPU, 8GB RAM): ~$50-70/month
- S3 storage: ~$1-5/month
- Data transfer: ~$10-20/month
- **Total**: ~$60-95/month

**Optimization Tips:**
- Use spot instances for non-critical workloads
- Implement auto-scaling based on usage
- Use CloudFront for caching
- Compress embeddings

## Maintenance

### Regular Tasks

**Daily:**
- Check logs for errors
- Monitor response times
- Review user feedback

**Weekly:**
- Backup data
- Update dependencies
- Review metrics

**Monthly:**
- Update models if needed
- Optimize performance
- Security audit

### Updates

**Updating Dataset:**
```bash
# 1. Add new data to FYP_dataset
# 2. Rerun preprocessing
python src/data_preprocessing.py

# 3. Regenerate embeddings
python src/embedding_generator.py

# 4. Rebuild vector store
python src/vector_store.py

# 5. Restart application
```

**Updating Models:**
```bash
# Update embedding model
# Edit config.yaml: embedding.model_name
# Regenerate embeddings

# Update LLM
# Edit config.yaml: llm.model_name
# Restart application
```

## Troubleshooting Production Issues

### High Memory Usage
- Enable quantization
- Reduce batch sizes
- Use model offloading

### Slow Response Times
- Add caching
- Use GPU instances
- Optimize retrieval (reduce top_k)

### Frequent Crashes
- Check logs for errors
- Increase memory limits
- Add health checks

### Poor Response Quality
- Review retrieved context
- Adjust retrieval parameters
- Update prompts

## Monitoring Dashboard

**Recommended Tools:**
- **Grafana**: Metrics visualization
- **Prometheus**: Metrics collection
- **ELK Stack**: Log aggregation
- **Sentry**: Error tracking

## Support and Maintenance

**Documentation:**
- Keep README updated
- Document all changes
- Maintain changelog

**User Support:**
- Collect feedback
- Track common issues
- Provide help documentation

**Continuous Improvement:**
- A/B test prompts
- Monitor user satisfaction
- Regular model updates

## Legal and Compliance

**Data Privacy:**
- Don't log personal information
- Implement data retention policies
- Comply with local regulations

**Disclaimers:**
- Clear legal disclaimers
- Terms of service
- Privacy policy

**Accessibility:**
- WCAG compliance
- Mobile responsiveness
- Multi-language support (future)

## Conclusion

Choose the deployment option that best fits your:
- Budget
- Technical expertise
- Scalability needs
- Privacy requirements

For most use cases, start with local deployment or Streamlit Cloud, then scale up as needed.
