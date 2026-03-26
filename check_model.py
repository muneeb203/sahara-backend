"""Check which Ollama models are installed."""

import ollama

try:
    models = ollama.list()
    print("Installed Ollama models:")
    print()
    print("Raw response:", models)
    print()
    
    if models.get('models'):
        for model in models['models']:
            print(f"Model: {model}")
            print()
    else:
        print("  No models installed")
        print()
        print("To install a model, run:")
        print("  ollama pull llama3")
        print("  or")
        print("  ollama pull llama3.2")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
