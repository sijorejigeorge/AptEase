import os
import sqlite3
import pandas as pd

def init_db(csv_path, db_name="apartments.db"):
    # Connect to SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Read the first chunk of the CSV to get the columns dynamically
    try:
        # Load a single chunk to inspect columns
        chunk = pd.read_csv(csv_path, engine='python', nrows=1, on_bad_lines='skip', quotechar='"', escapechar='\\')
        columns = chunk.columns.tolist()  # Get column names dynamically
    except Exception as e:
        print(f"Error reading the CSV header: {e}")
        conn.close()
        return

    # Create the table for apartment listings dynamically based on the CSV columns
    try:
        create_table_query = f'''
            CREATE TABLE IF NOT EXISTS listings (
                id INTEGER PRIMARY KEY,
                {", ".join([f"{col} TEXT" for col in columns])}
            )
        '''
        cursor.execute(create_table_query)
        conn.commit()
    except Exception as e:
        print(f"Error creating table: {e}")
        conn.close()
        return

    # Load data from CSV in chunks to handle large files
    try:
        chunk_size = 1000
        chunks = pd.read_csv(csv_path, engine='python', chunksize=chunk_size, on_bad_lines='skip', quotechar='"', escapechar='\\')
        for chunk in chunks:
            # Insert data chunk into the database dynamically
            chunk.to_sql('listings', conn, if_exists='append', index=False)
        print("Data successfully loaded into the database.")
    except Exception as e:
        print(f"Error loading data: {e}")
    finally:
        conn.close()

def clean_csv(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
            for line in infile:
                line = line.replace('"\n', '')  # Removes problematic trailing quotes
                line = line.replace('""', '"')  # Fixes double quotes
                outfile.write(line)
        print(f"CSV cleaned successfully: {output_path}")
    except Exception as e:
        print(f"Error cleaning CSV file: {e}")

# Use current directory for paths
current_folder = os.getcwd()
input_csv = os.path.join(current_folder, "airbnb_listings_cleaned.csv")
output_csv = os.path.join(current_folder, "airbnb-listings-cleaned.csv")

# Clean the CSV file and initialize the database
#clean_csv(input_csv, output_csv)
init_db(input_csv)
