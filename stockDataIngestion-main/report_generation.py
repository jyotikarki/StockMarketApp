import sqlite3
import pandas as pd

def generate_reports():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('stocks.db')

        # Define the SQL query
        query = '''
        SELECT symbol, date,close 
        FROM stocks
        WHERE date = (SELECT MAX(date) FROM stocks WHERE symbol = stocks.symbol)
        '''

        # Execute the query and fetch data into a DataFrame
        df = pd.read_sql_query(query, conn)
        
        # Print the columns of the DataFrame to debug
        print("Columns in DataFrame:", df.columns)

        # Close the database connection
        conn.close()

        # Check if the DataFrame is empty
        if df.empty:
            print("No data found for generating reports.")
            return

        # Generate and print daily report
        daily_report = df.groupby('symbol').agg({'close': 'last'})
        print("\nDaily Report:\n", daily_report)

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    generate_reports()
