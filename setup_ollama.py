"""Setup script to download and test Ollama LLaMA model."""

import ollama
import sys

def main():
    print("="*80)
    print("  Ollama Setup - Downloading LLaMA 3B Model")
    print("="*80)
    print()
    
    # Check if Ollama is running
    print("Step 1: Checking Ollama connection...")
    try:
        ollama.list()
        print("✓ Ollama is running!")
    except Exception as e:
        print(f"✗ Error: Cannot connect to Ollama")
        print(f"  Make sure Ollama is running")
        print(f"  Error: {e}")
        return
    
    print()
    print("Step 2: Checking if llama3:3b is already installed...")
    
    # Check if model exists
    models = ollama.list()
    model_exists = any('llama3:3b' in model['name'] for model in models.get('models', []))
    
    if model_exists:
        print("✓ llama3:3b is already installed!")
    else:
        print("Model not found. Downloading llama3:3b...")
        print("This will take 10-15 minutes (2GB download)")
        print()
        
        try:
            # Pull the model
            print("Downloading... (you'll see progress)")
            for progress in ollama.pull('llama3:3b', stream=True):
                if 'status' in progress:
                    print(f"\r{progress['status']}", end='', flush=True)
                if 'completed' in progress and 'total' in progress:
                    percent = (progress['completed'] / progress['total']) * 100
                    print(f"\rProgress: {percent:.1f}%", end='', flush=True)
            
            print()
            print("✓ Model downloaded successfully!")
        except Exception as e:
            print(f"\n✗ Error downloading model: {e}")
            return
    
    print()
    print("Step 3: Testing the model...")
    
    try:
        response = ollama.generate(
            model='llama3:3b',
            prompt='Say "Hello, I am ready!" in one sentence.',
            options={'num_predict': 50}
        )
        
        print("✓ Model test successful!")
        print(f"  Response: {response['response']}")
    except Exception as e:
        print(f"✗ Error testing model: {e}")
        return
    
    print()
    print("="*80)
    print("  Setup Complete! ✓")
    print("="*80)
    print()
    print("Your chatbot is ready to use!")
    print()
    print("To start the chatbot:")
    print("  1. Web interface: streamlit run app.py")
    print("  2. Command line: python src/chatbot.py")
    print()
    print("="*80)

if __name__ == "__main__":
    main()
