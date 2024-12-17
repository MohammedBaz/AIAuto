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
import streamlit as st
import google.generativeai as genai

st.title("Echo Bot")


genai.configure(api_key=st.secrets["GeminiKey"])
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt)
st.write(response.text)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    #response = f"Echo: {prompt}"
    response = model.generate_content(prompt)
    #st.write(response.text)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
