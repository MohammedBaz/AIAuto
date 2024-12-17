import streamlit as st
from model import configure_model, generate_response
from database import initialize_database, query_employees

# Initialize database
initialize_database()

# App title
st.title("Medical Institution Employee Bot")

# Initialize the Gemini model
if "model" not in st.session_state:
    api_key = st.secrets["GeminiKey"]
    st.session_state.model = configure_model(api_key)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask about employees by name, role, or department!"):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Query the employee database
    db_response = query_employees(prompt)
    if "No matching employees" not in db_response:
        response = db_response
    else:
        # If no match, fallback to the Gemini AI model
        response = generate_response(st.session_state.model, prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
