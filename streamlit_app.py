import streamlit as st
import sqlite3
import os
from google.generativeai import text

# Access API Key from Streamlit Secrets (CRUCIAL!)
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# Initialize Gemini
text.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Database setup (Medical Institution Data)
DATABASE_FILE = "medical_data.db"  # This will be created in the app's directory

def create_medical_database():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER,
                diagnosis TEXT,
                treatment TEXT,
                admission_date TEXT
            )
        """)
        sample_data = [
            ("John Doe", 45, "Hypertension", "Medication A", "2024-01-15"),
            ("Jane Smith", 62, "Diabetes", "Insulin therapy", "2023-11-20"),
            ("David Lee", 38, "Fractured Femur", "Surgery and physical therapy", "2024-02-01"),
            ("Sarah Jones", 55, "Migraine", "Medication B", "2024-03-10"),
            ("Michael Brown", 70, "Heart Failure", "Medication C and lifestyle changes", "2024-01-28")
        ]
        cursor.executemany("INSERT OR IGNORE INTO patients (name, age, diagnosis, treatment, admission_date) VALUES (?, ?, ?, ?, ?)", sample_data)
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

create_medical_database()

def get_gemini_sql(user_query):
    prompt = f"""
    Translate the following user query into a SQL query that can be executed against a database with a table named 'patients' having columns: patient_id (integer), name (text), age (integer), diagnosis (text), treatment (text), admission_date (text).

    User Query: {user_query}

    SQL Query:
    """
    try:
        response = text.generate_text(
            model="gemini/gemini-pro",
            prompt=prompt,
            temperature=0.0,
            max_output_tokens=256
        )
        sql_query = response.result.strip()
        return sql_query
    except Exception as e:
        st.error(f"Gemini API Error: {e}")
        return None

def execute_query(sql_query):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        st.error(f"SQL Execution Error: {e}")
        return None
    finally:
        if conn:
            conn.close()


st.title("Medical Data Query with Gemini")

user_query = st.text_input("Enter your medical data query (e.g., What is the diagnosis of John Doe?)")

if st.button("Submit"):
    if user_query:
        sql_query = get_gemini_sql(user_query)
        if sql_query:
            st.code(sql_query, language="sql")
            results = execute_query(sql_query)
            if results is not None:
                if results:
                    st.write("Query Results:")
                    st.table(results)
                else:
                    st.write("No results found.")
    else:
        st.warning("Please enter a query.")
