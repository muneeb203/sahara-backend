"""LLaMA 3B interface for text generation."""

import logging
import os
from typing import Dict, Optional
import requests
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

from utils import load_config


logger = logging.getLogger(__name__)


class LLaMAInterface:
    """Interface for LLaMA 3B model."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.llm_config = config['llm']
        self.hf_api_token = os.getenv("HF_API_TOKEN")
        self.hf_api_model = os.getenv("HF_API_MODEL", self.llm_config.get("model_name"))
        self.hf_api_timeout = int(os.getenv("HF_API_TIMEOUT", "120"))
        
        # Check if using Ollama
        self.use_ollama = self.llm_config.get('use_ollama', False)
        self.use_hf_inference_api = bool(self.hf_api_token) and not self.use_ollama
        
        if self.use_ollama:
            self._init_ollama()
        elif self.use_hf_inference_api:
            logger.info(f"Using Hugging Face Inference API model: {self.hf_api_model}")
        else:
            self._init_huggingface()
    
    def _init_ollama(self):
        """Initialize Ollama client."""
        try:
            ollama_base_url = self.llm_config.get("ollama_base_url")
            if ollama_base_url:
                os.environ["OLLAMA_HOST"] = ollama_base_url

            import ollama
            self.ollama_client = ollama
            # Use llama3:latest (or llama3) which is what's actually installed
            self.model_name = "llama3:latest"
            logger.info(f"Initialized Ollama client with model: {self.model_name}")
        except ImportError:
            logger.error("Ollama not installed. Install with: pip install ollama")
            raise
    
    def _init_huggingface(self):
        """Initialize Hugging Face model."""
        model_name = self.llm_config['model_name']
        logger.info(f"Loading LLaMA model: {model_name}")
        
        # Quantization config
        quantization_config = None
        if self.llm_config.get('load_in_8bit', False):
            quantization_config = BitsAndBytesConfig(load_in_8bit=True)
            logger.info("Using 8-bit quantization")
        elif self.llm_config.get('load_in_4bit', False):
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16
            )
            logger.info("Using 4-bit quantization")
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Load model
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=quantization_config,
            device_map="auto",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        )
        
        logger.info("Model loaded successfully")
    
    def generate_ollama(self, prompt: str) -> str:
        """Generate response using Ollama."""
        try:
            response = self.ollama_client.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    'temperature': self.llm_config['temperature'],
                    'top_p': self.llm_config['top_p'],
                    'num_predict': self.llm_config['max_new_tokens']
                }
            )
            return response['response']
        except Exception as e:
            logger.error(f"Ollama generation error: {e}")
            return "I apologize, but I'm having trouble generating a response. Please try again."
    
    def generate_huggingface(self, prompt: str) -> str:
        """Generate response using Hugging Face model."""
        try:
            # Tokenize
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
            
            # Move to device
            if torch.cuda.is_available():
                inputs = {k: v.to('cuda') for k, v in inputs.items()}
            
            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=self.llm_config['max_new_tokens'],
                    temperature=self.llm_config['temperature'],
                    top_p=self.llm_config['top_p'],
                    do_sample=self.llm_config['do_sample'],
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Remove the prompt from response
            if response.startswith(prompt):
                response = response[len(prompt):].strip()
            
            return response
        
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return "I apologize, but I'm having trouble generating a response. Please try again."

    def generate_hf_api(self, prompt: str) -> str:
        """Generate response using Hugging Face Inference API."""
        try:
            url = f"https://api-inference.huggingface.co/models/{self.hf_api_model}"
            headers = {"Authorization": f"Bearer {self.hf_api_token}"}
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": self.llm_config['max_new_tokens'],
                    "temperature": self.llm_config['temperature'],
                    "top_p": self.llm_config['top_p'],
                    "do_sample": self.llm_config['do_sample'],
                    "return_full_text": False,
                },
            }

            response = requests.post(url, headers=headers, json=payload, timeout=self.hf_api_timeout)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                generated = data[0].get("generated_text", "").strip()
                if generated:
                    return generated

            if isinstance(data, dict) and data.get("error"):
                raise RuntimeError(data["error"])

            return "I apologize, but I could not generate a complete response right now."
        except Exception as e:
            logger.error(f"Hugging Face API generation error: {e}")
            return "I apologize, but I'm having trouble generating a response. Please try again."
    
    def generate(self, prompt: str) -> str:
        """Generate response (unified interface)."""
        if self.use_ollama:
            return self.generate_ollama(prompt)
        elif self.use_hf_inference_api:
            return self.generate_hf_api(prompt)
        else:
            return self.generate_huggingface(prompt)
    
    def format_prompt(self, system_prompt: str, user_message: str, context: str) -> str:
        """Format prompt for LLaMA."""
        # LLaMA 3 chat format
        prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>

Context from knowledge base:
{context}

User Question: {user_message}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

"""
        return prompt


def main():
    """Test LLaMA interface."""
    logging.basicConfig(level=logging.INFO)
    
    config = load_config()
    llm = LLaMAInterface(config)
    
    # Test generation
    system_prompt = config['prompts']['system_prompt']
    test_context = "According to the Muslim Family Laws Ordinance, 1961, Section 6, a man must obtain permission from an Arbitration Council before contracting another marriage."
    test_question = "Can my husband marry another woman without my permission?"
    
    prompt = llm.format_prompt(system_prompt, test_question, test_context)
    
    print("Generating response...")
    response = llm.generate(prompt)
    
    print("\n" + "="*80)
    print("Response:")
    print("="*80)
    print(response)


if __name__ == "__main__":
    main()
