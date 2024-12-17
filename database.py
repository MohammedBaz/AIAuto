import sqlite3

# Function to initialize the database with the Employees table
def initialize_database():
    conn = sqlite3.connect("medical_employees.db")
    cursor = conn.cursor()
    
    # Create the Employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            department TEXT NOT NULL,
            contact_number TEXT,
            email TEXT,
            hire_date TEXT,
            salary REAL
        )
    ''')
    conn.commit()
    
    # Insert sample data if the table is empty
    cursor.execute("SELECT COUNT(*) FROM employees")
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
            INSERT INTO employees (name, role, department, contact_number, email, hire_date, salary)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', [
            ("Dr. Alice Smith", "Doctor", "Cardiology", "555-1234", "alice.smith@hospital.com", "2020-01-15", 12000.0),
            ("John Doe", "Nurse", "ICU", "555-5678", "john.doe@hospital.com", "2018-03-22", 5000.0),
            ("Dr. Bob Johnson", "Surgeon", "Surgery", "555-9876", "bob.johnson@hospital.com", "2019-06-01", 15000.0),
            ("Mary Lee", "Technician", "Radiology", "555-4321", "mary.lee@hospital.com", "2021-09-10", 4000.0),
            ("Sarah Kim", "Receptionist", "Administration", "555-2468", "sarah.kim@hospital.com", "2022-01-05", 3000.0),
        ])
        conn.commit()
    conn.close()

# Function to query employees by name, role, or department
def query_employees(query):
    conn = sqlite3.connect("medical_employees.db")
    cursor = conn.cursor()
    
    # Search for employees based on input (flexible search)
    cursor.execute('''
        SELECT name, role, department, contact_number, email, hire_date, salary 
        FROM employees 
        WHERE name LIKE ? OR role LIKE ? OR department LIKE ?
    ''', (f"%{query}%", f"%{query}%", f"%{query}%"))
    
    results = cursor.fetchall()
    conn.close()
    
    # Format and return results
    if results:
        response = "**Employee Details:**\n"
        for row in results:
            response += (
                f"- **Name:** {row[0]}\n"
                f"  **Role:** {row[1]}\n"
                f"  **Department:** {row[2]}\n"
                f"  **Contact:** {row[3]}\n"
                f"  **Email:** {row[4]}\n"
                f"  **Hire Date:** {row[5]}\n"
                f"  **Salary:** ${row[6]:,.2f}\n\n"
            )
        return response
    else:
        return "No matching employees found in the database."
