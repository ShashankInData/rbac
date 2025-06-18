import streamlit as st
import requests
import json
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="RBAC Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .bot-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# API configuration
API_BASE_URL = "http://localhost:8000"

def login(username, password):
    """Login to the API and get access token"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/auth/login",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("access_token"), "success"
        else:
            return None, f"Login failed: {response.text}"
    except Exception as e:
        return None, f"Connection error: {str(e)}"

def send_message(message, token):
    """Send message to the API"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{API_BASE_URL}/api/v1/chat/query",
            headers=headers,
            json={"message": message}
        )
        if response.status_code == 200:
            return response.json(), "success"
        else:
            return None, f"Error: {response.text}"
    except Exception as e:
        return None, f"Connection error: {str(e)}"

# Main app
def main():
    # Header with banner image
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        banner_path = Path("resources/RPC_01_Thumbnail.jpg")
        if banner_path.exists():
            st.image(str(banner_path), use_container_width=True)
        else:
            st.markdown("""
            <div class="main-header">
                <h1>🤖 RBAC Chatbot</h1>
                <p>Role-Based Access Control Document Assistant</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sidebar for login
    with st.sidebar:
        st.header("🔐 Authentication")
        
        if st.session_state.token is None:
            st.subheader("Login")
            username = st.text_input("Username", value="Tony")
            password = st.text_input("Password", type="password", value="password123")
            
            if st.button("Login"):
                token, message = login(username, password)
                if token:
                    st.session_state.token = token
                    st.session_state.user_role = "engineering"  # Default for Tony
                    st.session_state.username = username  # Store username in session
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error(message)
        else:
            # Use username from session state
            st.success(f"Logged in as: {st.session_state.get('username', 'User')}")
            st.info(f"Role: {st.session_state.user_role}")
            if st.button("Logout"):
                st.session_state.token = None
                st.session_state.user_role = None
                st.session_state.username = None
                st.session_state.messages = []
                st.rerun()
        
        st.markdown("---")
        st.subheader("ℹ️ About")
        st.markdown("""
        This chatbot provides role-based access to company documents:
        
        - **Engineering**: Access to technical docs
        - **Finance**: Access to financial reports
        - **HR**: Access to employee policies
        - **Marketing**: Access to marketing materials
        
        Ask questions about topics relevant to your role!
        """)
    
    # Main chat interface
    if st.session_state.token is None:
        st.warning("Please login to start chatting!")
        return
    
    # Chat title
    st.header("💬 Chat Interface")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message and message["sources"]:
                st.caption(f"Sources: {', '.join(message['sources'])}")
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about your documents..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response, error = send_message(prompt, st.session_state.token)
                
                if error == "success":
                    bot_response = response.get("response", "No response received")
                    sources = response.get("sources", [])
                    
                    st.markdown(bot_response)
                    if sources:
                        st.caption(f"Sources: {', '.join(sources)}")
                    
                    # Add bot message to chat history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": bot_response,
                        "sources": sources
                    })
                else:
                    st.error(f"Error: {error}")
    
    # Clear chat button
    if st.session_state.messages and st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main() 