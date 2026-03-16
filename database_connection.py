"""
SQL Server Connection Setup
Server: STRANGER\SQLEXPRESS
Authentication: Windows Authentication (Integrated)
"""

import pyodbc
import pandas as pd
from sqlalchemy import create_engine

# Connection String for Windows Authentication
SERVER = 'STRANGER\\SQLEXPRESS'
DATABASE = ''  # Leave empty for default database, or specify database name

# Method 1: Using pyodbc
def connect_with_pyodbc():
    """Connect using pyodbc"""
    conn_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};Trusted_Connection=yes;'
    try:
        conn = pyodbc.connect(conn_string)
        print("✓ Connected to SQL Server using pyodbc")
        return conn
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return None

# Method 2: Using SQLAlchemy (recommended for pandas)
def connect_with_sqlalchemy():
    """Connect using SQLAlchemy"""
    try:
        engine = create_engine(f'mssql+pyodbc://{SERVER}/master?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes')
        print("✓ Connected to SQL Server using SQLAlchemy")
        return engine
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return None

# Example: Run a query
def run_query(engine, query):
    """Execute a SQL query and return results as DataFrame"""
    try:
        df = pd.read_sql_query(query, engine)
        return df
    except Exception as e:
        print(f"✗ Query failed: {e}")
        return None

# Test the connection
if __name__ == "__main__":
    # Test SQLAlchemy connection
    engine = connect_with_sqlalchemy()
    
    if engine:
        # Example: List databases
        query = "SELECT name FROM sys.databases"
        result = run_query(engine, query)
        if result is not None:
            print("\nAvailable Databases:")
            print(result)
