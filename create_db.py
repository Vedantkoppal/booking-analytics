import pandas as pd
from app.core.data_config import DB_URI, BOOKING_DATA
from sqlalchemy import create_engine, text

# Load data from CSV
df = pd.read_csv(BOOKING_DATA)

# Create DB engine
engine = create_engine(DB_URI)

# Convert the DataFrame to a SQL table
df.to_sql('my_table', con=engine, if_exists='replace', index=False)
print("Data inserted successfully")

with engine.connect() as con:
    # Check number of rows
    rs = con.execute(text('SELECT COUNT(*) FROM my_table'))
    rows = rs.scalar()

    # SELECT 1 command to check DB connectivity
    rs_1 = con.execute(text('SELECT 1'))
    result_1 = rs_1.scalar()

    # Get the list of tables for SQLite
    rs_tables = con.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
    tables = [row[0] for row in rs_tables.fetchall()]

print(f"Tables in the database: {tables}")
print(f"Number of Rows: {rows}")
print(f"SELECT 1 result: {result_1}")
