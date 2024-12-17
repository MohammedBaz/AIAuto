import streamlit as st
from model import configure_model, generate_response

# App title
st.title("Echo Bot")

# Initialize the Gemini model
if "model" not in st.session_state:
    api_key = st.secrets["GeminiKey"]  # Fetch API key securely
    st.session_state.model = configure_model(api_key)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What is up?"):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Generate response using the model
    response = generate_response(st.session_state.model, prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
