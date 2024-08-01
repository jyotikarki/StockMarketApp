import sqlite3

# # Connect to an SQLite database
# conn = sqlite3.connect('/home/sigmoid/Desktop/TechDemo_final/StockMarketApp-main/db.sqlite3)
#
# # Create a cursor object
# cursor = conn.cursor()
#
# # Query to list all tables
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# cursor.execute("SELECT *  FROM stocks limit 10;")
# # Fetch all results
# tables = cursor.fetchall()
#
# # Print the tables
# print("index","symbol", "date", "open","high" , "low", "close", "volume")
# for table in tables:
#     # print(table[0])
#     print(table[0],table[1],table[2],table[3],table[4],table[5],table[6],table[7])
#
# # Close the connection
# conn.close()

def show_schema(database_uri):
    # Connect to the SQLite database
    connection = sqlite3.connect(database_uri)
    cursor = connection.cursor()

    # Get the list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table_name in tables:
        print(f"Table: {table_name[0]}")

        # Get schema for each table
        cursor.execute(f"PRAGMA table_info({table_name[0]});")
        schema = cursor.fetchall()

        for column in schema:
            print(f"Column: {column[1]}, Type: {column[2]}, Not Null: {column[3]}, Default Value: {column[4]}")

        print("-" * 40)

    # Close the connection
    connection.close()

# Example usage
DATABASE_URI = 'roject/db.sqlite3'
show_schema(DATABASE_URI)
