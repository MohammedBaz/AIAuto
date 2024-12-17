import streamlit as st
from database import execute_sql_query
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=st.secrets["GeminiKey"])
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to generate SQL query from natural language
def generate_sql_query(prompt):
    sql_prompt = f"""
    You are an AI assistant that generates SQL queries for a SQLite database.
    The database has an 'employees' table with the following columns:
    - id (integer)
    - name (text)
    - role (text)
    - department (text)
    - salary (integer)

    Convert the following natural language question into a valid SQL query:
    "{prompt}"
    Only return the SQL query without explanation.
    """
    response = model.generate_content(sql_prompt)
    return response.text.strip()

# Streamlit UI
st.title("Medical Institution Query Bot")

# Display messages from chat history on app rerun
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if user_input := st.chat_input("Ask about doctors, employees, or departments:"):
    # Add user input to chat history
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate SQL query from user input
    sql_query = generate_sql_query(user_input)
    st.write(f"Generated SQL Query: `{sql_query}`")  # Optional for debugging

    # Execute the SQL query
    result = execute_sql_query(sql_query)

    # Format and display results
    if isinstance(result, list) and len(result) > 0:
        formatted_result = "\n".join([str(row) for row in result])
        response = f"Query Results:\n{formatted_result}"
    elif isinstance(result, str):  # Handle error message
        response = result
    else:
        response = "No matching data found."

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
