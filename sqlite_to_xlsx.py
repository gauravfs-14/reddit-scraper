import sqlite3
import pandas as pd
import os
from datetime import datetime

def sqlite_to_xlsx(db_path, output_dir=None):
    """
    Convert SQLite database to Excel file
    
    Args:
        db_path (str): Path to SQLite database file
        output_dir (str): Directory to save Excel file (defaults to same dir as DB)
    
    Returns:
        str: Path to the created Excel file
    """
    # Validate input database exists
    if not os.path.exists(db_path):
        print(f"Error: Database file {db_path} not found.")
        return None
        
    # Set output directory
    if output_dir is None:
        output_dir = os.path.dirname(db_path)
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate output filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(os.path.basename(db_path))[0]
    output_file = os.path.join(output_dir, f"{base_name}_{timestamp}.xlsx")
    
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(db_path)
        
        # Get list of tables
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        # Create Excel writer
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Convert each table to Excel sheet
            for table in tables:
                table_name = table[0]
                print(f"Processing table: {table_name}")
                
                # Read table into pandas DataFrame
                df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                
                # Convert UNIX timestamps to readable dates if created_utc exists
                if 'created_utc' in df.columns:
                    df['created_date'] = pd.to_datetime(df['created_utc'], unit='s')
                
                # Write DataFrame to Excel sheet
                df.to_excel(writer, sheet_name=table_name, index=False)
                
                # Add summary information
                print(f"  - Exported {len(df)} rows")
        
        conn.close()
        print(f"\nExcel file created successfully: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"Error converting database to Excel: {e}")
        return None

if __name__ == "__main__":
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Default database path (in the same directory)
    default_db_path = os.path.join(current_dir, "reddit_posts.db")
    
    # If database exists, convert it
    if os.path.exists(default_db_path):
        print(f"Converting {default_db_path} to Excel...")
        output_file = sqlite_to_xlsx(default_db_path)
        
        if output_file:
            file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
            print(f"Conversion complete! File size: {file_size_mb:.2f} MB")
    else:
        print(f"Database file not found: {default_db_path}")
        print("Please ensure you've run main.py to scrape and create the database first.")