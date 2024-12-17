import streamlit as st
import google.generativeai as genai

# Configure API
genai.configure(api_key=st.secrets["GeminiKey"])
model = genai.GenerativeModel("gemini-1.5-flash")

# App title
st.title("Echo Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process user input
if prompt := st.chat_input("What is up?"):
    # Add user input to chat history
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response
    response = model.generate_content(prompt).text

    # Display and store assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
