"""Check Ollama status and available models."""

import ollama

print("Checking Ollama...")
print()

try:
    # List installed models
    models = ollama.list()
    print("Installed models:")
    if models.get('models'):
        for model in models['models']:
            print(f"  - {model['name']}")
    else:
        print("  No models installed yet")
    
    print()
    print("Attempting to pull llama3...")
    
    # Try pulling llama3 (without version tag)
    for progress in ollama.pull('llama3', stream=True):
        if 'status' in progress:
            print(f"\r{progress['status']}", end='', flush=True)
    
    print()
    print("Success!")
    
except Exception as e:
    print(f"Error: {e}")
    print()
    print("Trying alternative: llama3.2:3b")
    
    try:
        for progress in ollama.pull('llama3.2:3b', stream=True):
            if 'status' in progress:
                print(f"\r{progress['status']}", end='', flush=True)
        print()
        print("Success!")
    except Exception as e2:
        print(f"Error: {e2}")
