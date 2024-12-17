import sqlite3

# Initialize database and create employees table
def initialize_database():
    conn = sqlite3.connect("medical_employees.db")
    cursor = conn.cursor()

    # Create the employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            department TEXT NOT NULL,
            salary INTEGER NOT NULL
        )
    ''')

    # Insert sample data
    cursor.execute("DELETE FROM employees")  # Clear previous data (optional)
    sample_data = [
        ("Dr. John Smith", "doctor", "Cardiology", 150000),
        ("Dr. Jane Doe", "doctor", "Neurology", 145000),
        ("Alice Brown", "Nurse", "Cardiology", 75000),
        ("Bob White", "Technician", "Radiology", 65000),
        ("Dr. Emily Green", "doctor", "Pediatrics", 140000),
        ("Charlie Black", "Administrator", "Administration", 80000)
    ]

    cursor.executemany('INSERT INTO employees (name, role, department, salary) VALUES (?, ?, ?, ?)', sample_data)
    conn.commit()
    conn.close()

# Function to execute any dynamic SQL query
def execute_sql_query(query):
    try:
        conn = sqlite3.connect("medical_employees.db")
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result
    except Exception as e:
        return f"Error executing query: {str(e)}"

if __name__ == "__main__":
    initialize_database()
    print("Database initialized with sample data.")
