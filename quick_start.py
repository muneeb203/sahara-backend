"""Quick start script to set up the HerHaq chatbot."""

import subprocess
import sys
from pathlib import Path
import os


def print_header(text):
    """Print formatted header."""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"→ {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✓ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error during {description}:")
        print(e.stderr)
        return False


def check_prerequisites():
    """Check if prerequisites are met."""
    print_header("Checking Prerequisites")
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("✗ Python 3.8 or higher is required!")
        return False
    print("✓ Python version OK")
    
    # Check if FYP_dataset exists
    dataset_path = Path("../FYP_dataset")
    if not dataset_path.exists():
        print(f"✗ Dataset not found at {dataset_path.absolute()}")
        print("  Please ensure FYP_dataset folder is in the parent directory")
        return False
    print("✓ Dataset found")
    
    return True


def install_dependencies():
    """Install required packages."""
    print_header("Installing Dependencies")
    
    print("This may take several minutes...")
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing packages"
    )


def setup_directories():
    """Create necessary directories."""
    print_header("Setting Up Directories")
    
    dirs = [
        "data/processed",
        "embeddings",
        "logs"
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created {dir_path}")
    
    return True


def run_preprocessing():
    """Run data preprocessing."""
    print_header("Step 1: Data Preprocessing")
    
    print("Cleaning and chunking the dataset...")
    print("This will take 2-5 minutes.\n")
    
    return run_command(
        f"{sys.executable} src/data_preprocessing.py",
        "Data preprocessing"
    )


def run_embedding_generation():
    """Generate embeddings."""
    print_header("Step 2: Embedding Generation")
    
    print("Generating vector embeddings for semantic search...")
    print("This will take 5-15 minutes depending on your hardware.\n")
    
    return run_command(
        f"{sys.executable} src/embedding_generator.py",
        "Embedding generation"
    )


def run_vector_store_creation():
    """Create vector store."""
    print_header("Step 3: Vector Store Creation")
    
    print("Building FAISS index for fast retrieval...")
    print("This will take 1-2 minutes.\n")
    
    return run_command(
        f"{sys.executable} src/vector_store.py",
        "Vector store creation"
    )


def run_tests():
    """Run pipeline tests."""
    print_header("Step 4: Testing Pipeline")
    
    print("Running tests to verify the setup...")
    print("Note: Full LLM test will be skipped in quick start.\n")
    
    # Run test without LLM
    return run_command(
        f"{sys.executable} test_pipeline.py",
        "Pipeline testing"
    )


def print_next_steps():
    """Print next steps."""
    print_header("Setup Complete! 🎉")
    
    print("Your HerHaq chatbot is ready to use!\n")
    
    print("Next Steps:")
    print("\n1. Run the chatbot in CLI mode:")
    print(f"   {sys.executable} src/chatbot.py")
    
    print("\n2. Run the web interface (Recommended):")
    print("   streamlit run app.py")
    
    print("\n3. Configure LLaMA model:")
    print("   - Option A: Use Ollama (easier)")
    print("     • Install Ollama from https://ollama.ai")
    print("     • Run: ollama pull llama3:3b")
    print("     • Update config.yaml: use_ollama: true")
    
    print("\n   - Option B: Use Hugging Face")
    print("     • Login: huggingface-cli login")
    print("     • Accept license at: https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct")
    
    print("\n4. Read the documentation:")
    print("   - SETUP_GUIDE.md - Detailed setup instructions")
    print("   - DOCUMENTATION.md - Technical documentation")
    print("   - README.md - Project overview")
    
    print("\n" + "="*80)
    print("For help, see SETUP_GUIDE.md or DOCUMENTATION.md")
    print("="*80 + "\n")


def main():
    """Main quick start function."""
    print("\n" + "="*80)
    print("  HerHaq Chatbot - Quick Start Setup")
    print("  This script will set up the complete RAG pipeline")
    print("="*80)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n✗ Prerequisites check failed. Please fix the issues and try again.")
        return
    
    # Ask for confirmation
    print("\nThis script will:")
    print("  1. Install Python dependencies")
    print("  2. Process the dataset")
    print("  3. Generate embeddings")
    print("  4. Build vector store")
    print("  5. Run tests")
    print("\nEstimated time: 15-30 minutes")
    
    response = input("\nContinue? (y/n): ").strip().lower()
    if response != 'y':
        print("Setup cancelled.")
        return
    
    # Run setup steps
    steps = [
        (install_dependencies, "Installing dependencies"),
        (setup_directories, "Setting up directories"),
        (run_preprocessing, "Data preprocessing"),
        (run_embedding_generation, "Embedding generation"),
        (run_vector_store_creation, "Vector store creation"),
        (run_tests, "Testing pipeline")
    ]
    
    for step_func, step_name in steps:
        if not step_func():
            print(f"\n✗ Setup failed at: {step_name}")
            print("Please check the error messages above and try again.")
            return
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user.")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        print("Please check the error and try again.")
