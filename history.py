# history.py
import streamlit as st

def init_history():
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

def add_history_item(title, content):
    """Add a new item to the chat history."""
    st.session_state.chat_history.append({'title': title, 'content': content})

def get_history():
    """Return the current chat history."""
    return st.session_state.get('chat_history', [])
