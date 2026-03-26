"""Streamlit web interface for HerHaq Chatbot."""

import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from chatbot import HerHaqChatbot
from utils import load_config, setup_logging


# Page configuration
st.set_page_config(
    page_title="HerHaq - Women's Rights Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #8B4789;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        padding-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #E8F4F8;
        border-left: 4px solid #2196F3;
    }
    .bot-message {
        background-color: #F3E8F8;
        border-left: 4px solid: #8B4789;
    }
    .source-box {
        background-color: #F5F5F5;
        padding: 0.5rem;
        border-radius: 0.3rem;
        margin-top: 0.5rem;
        font-size: 0.9rem;
    }
    .warning-box {
        background-color: #FFF3CD;
        border: 1px solid #FFC107;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_chatbot():
    """Load chatbot (cached)."""
    setup_logging()
    config = load_config()
    return HerHaqChatbot(config)


def display_message(role: str, content: str, sources: list = None):
    """Display a chat message."""
    if role == "user":
        st.markdown(f'<div class="chat-message user-message"><strong>You:</strong><br>{content}</div>', 
                   unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message bot-message"><strong>HerHaq:</strong><br>{content}</div>', 
                   unsafe_allow_html=True)
        
        # Display sources if available
        if sources:
            with st.expander("📚 View Sources"):
                for idx, source in enumerate(sources, 1):
                    st.markdown(f"**{idx}.** {source['citation']} (Relevance: {source['score']:.2f})")


def main():
    """Main Streamlit app."""
    
    # Header
    st.markdown('<h1 class="main-header">⚖️ HerHaq - Women\'s Rights Assistant</h1>', 
               unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your guide to understanding rights under Pakistani law and Islamic guidance</p>', 
               unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/8B4789/FFFFFF?text=HerHaq", use_column_width=True)
        
        st.markdown("### About HerHaq")
        st.info(
            "HerHaq is an AI-powered assistant that helps women understand their rights "
            "based on Pakistani laws, case studies, and Islamic ahadith. "
            "All responses include source citations for verification."
        )
        
        st.markdown("### Topics Covered")
        st.markdown("""
        - 👨‍👩‍👧 Marriage & Family Rights
        - 🏠 Inheritance & Property
        - 💼 Workplace Harassment
        - ⚖️ Legal Protections
        - 📖 Islamic Guidance
        - 📋 Case Studies
        """)
        
        st.markdown("### Example Questions")
        example_questions = [
            "What are my inheritance rights?",
            "How can I file a harassment complaint?",
            "Can my husband divorce me without consent?",
            "What does Islam say about women's property rights?",
            "What are the penalties for domestic violence?"
        ]
        
        for question in example_questions:
            if st.button(question, key=question):
                st.session_state.example_question = question
        
        st.markdown("---")
        
        if st.button("🗑️ Clear Conversation"):
            st.session_state.messages = []
            st.session_state.chatbot.clear_history()
            st.rerun()
        
        st.markdown("---")
        st.markdown("### ⚠️ Important Notice")
        st.warning(
            "This chatbot provides educational information only. "
            "For legal matters, please consult a qualified lawyer. "
            "In emergencies, contact local authorities."
        )
        
        st.markdown("### 📞 Emergency Contacts")
        st.markdown("""
        - **Emergency**: 1122
        - **Women Helpline**: 1099
        - **Rozan**: 0800-22222
        - **Police**: 15
        """)
    
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'chatbot' not in st.session_state:
        with st.spinner("Loading HerHaq Chatbot... This may take a moment."):
            st.session_state.chatbot = load_chatbot()
    
    # Display chat history
    for message in st.session_state.messages:
        display_message(
            message['role'],
            message['content'],
            message.get('sources')
        )
    
    # Handle example question
    if 'example_question' in st.session_state:
        user_input = st.session_state.example_question
        del st.session_state.example_question
    else:
        # Chat input
        user_input = st.chat_input("Ask me about your rights...")
    
    # Process user input
    if user_input:
        # Add user message to history
        st.session_state.messages.append({
            'role': 'user',
            'content': user_input,
            'sources': None
        })
        
        # Display user message
        display_message('user', user_input)
        
        # Get bot response
        with st.spinner("Thinking..."):
            result = st.session_state.chatbot.chat(user_input)
        
        # Add bot response to history
        st.session_state.messages.append({
            'role': 'assistant',
            'content': result['response'],
            'sources': result['sources']
        })
        
        # Display bot response
        display_message('assistant', result['response'], result['sources'])
        
        # Rerun to update chat
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #666; font-size: 0.9rem;">'
        'HerHaq Chatbot | Powered by LLaMA 3B & RAG | '
        'Built for women\'s empowerment'
        '</p>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
