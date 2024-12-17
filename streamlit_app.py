import streamlit as st
import sqlite3
import google.generativeai as genai

# Set up the API Key for Google Gemini
genai.configure(api_key=st.secrets["GeminiKey"])

# Function to get SQL query from Gemini API
def generate_sql_query(user_prompt):
    # Define a prompt template
    system_instruction = """
    You are an expert in converting natural language prompts to SQL queries.
    Based on the following user prompt, generate the correct SQL query. 
    Make sure the query is valid and adheres to SQLite syntax.
    """

    model = genai.GenerativeModel("gemini-pro")  # Use the gemini-pro model

    # Combine system instructions and user input
    full_prompt = f"{system_instruction}\n\nUser prompt: {user_prompt}\nSQL query:"

    # Call Gemini API
    response = model.generate_content(full_prompt)

    # Extract generated SQL query
    sql_query = response.text.strip()
    return sql_query

# Function to execute the generated SQL query on a database
def execute_sql_query(query, db_file="example.db"):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result
    except Exception as e:
        return f"Error: {e}"

# Streamlit App
st.title("Natural Language to SQL Converter (Powered by Gemini)")

# User input
user_prompt = st.text_area("Enter your query in plain English:", "Show all employees who earn more than 5000.")

# Generate SQL query button
if st.button("Generate SQL Query"):
    with st.spinner("Generating SQL Query..."):
        sql_query = generate_sql_query(user_prompt)
        st.code(sql_query, language="sql")
        st.success("SQL Query Generated Successfully!")

    # Execute SQL Query
    if st.checkbox("Execute this SQL Query on Database"):
        result = execute_sql_query(sql_query)
        st.write("### Query Result:")
        st.write(result)
