import sqlite3
import yahoo_fin.stock_info as yahooFinance
import datetime
from datetime import datetime, timedelta

def fetch_daily_closing_price(symbol):

    conn = sqlite3.connect('/app/db.sqlite3')

    c = conn.cursor()
    query = """
    SELECT date, close 
    FROM stocks 
    WHERE symbol = ? 
    ORDER BY date DESC 
    LIMIT 1
    """
    c.execute(query, (symbol,))
    result = c.fetchone()
    conn.close()
    return result

def fetch_price_change_percentage(symbol, days):

    conn = sqlite3.connect('/app/db.sqlite3')

    c = conn.cursor()
    end_date = datetime.now()
    start_date = (end_date - timedelta(days=days)).strftime('%Y-%m-%d')
    query = """
    SELECT (SELECT close FROM stocks 
            WHERE symbol = ? AND date = (SELECT MIN(date) FROM stocks WHERE symbol = ? AND date >= ?)) AS start_price,
           (SELECT close FROM stocks 
            WHERE symbol = ? AND date = (SELECT MAX(date) FROM stocks WHERE symbol = ? AND date <= ?)) AS end_price
    """
    c.execute(query, (symbol, symbol, start_date, symbol, symbol, end_date.strftime('%Y-%m-%d')))
    result = c.fetchone()
    conn.close()

    if result and result[0] and result[1]:
        start_price, end_price = result
        percentage_change = ((end_price - start_price) / start_price) * 100
        return percentage_change
    return None

def fetch_top_gainers_losers(period_days):

    conn = sqlite3.connect('/app/db.sqlite3')

    c = conn.cursor()
    end_date = datetime.now()
    start_date = (end_date - timedelta(days=period_days)).strftime('%Y-%m-%d')

    query = """
    SELECT symbol, 
           (MAX(close) - MIN(close)) AS price_change,
           (SELECT (MAX(close) - MIN(close)) / MIN(close) * 100 FROM stocks WHERE symbol = s.symbol AND date BETWEEN ? AND ?) AS percentage_change
    FROM stocks s
    WHERE date BETWEEN ? AND ? 
    GROUP BY symbol 
    ORDER BY price_change DESC
    """
    c.execute(query, (start_date, end_date.strftime('%Y-%m-%d'), start_date, end_date.strftime('%Y-%m-%d')))
    results = c.fetchall()
    conn.close()

    if results:
        top_gainers = results[:5]  # Top 5 gainers
        top_losers = results[-5:]  # Top 5 losers
        return top_gainers, top_losers
    return None, None

def display_and_save_kpis(symbol):
    print(f"KPIs for {symbol}:")

    # Daily Closing Price
    closing_price = fetch_daily_closing_price(symbol)
    if (closing_price is not None) and (closing_price[0] is not None):
        daily_closing_price = closing_price[1]
        print(f"Daily Closing Price: {daily_closing_price} on {closing_price[0]}")
    else:
        daily_closing_price = None

    # Price Change Percentage
    change_1day = fetch_price_change_percentage(symbol, 1)
    change_30days = fetch_price_change_percentage(symbol, 30)
    change_365days = fetch_price_change_percentage(symbol, 365)

    if change_1day is not None and change_30days is not None and change_365days is not None:
        print(f"Price Change Percentage over 1 day: {change_1day:.2f}%")
        print(f"Price Change Percentage over 30 days: {change_30days:.2f}%")
        print(f"Price Change Percentage over 365 days: {change_365days:.2f}%")
        insert_symbol_performance(symbol, daily_closing_price, change_1day, change_30days, change_365days)

def get_database_connection():
    return sqlite3.connect('/app/db.sqlite3')

def create_kpi_tables():
    conn = sqlite3.connect('/app/db.sqlite3')
    c = conn.cursor()

    # Table for symbol performance
    c.execute('''CREATE TABLE IF NOT EXISTS myapp_symbolperformance (
                    symbol TEXT PRIMARY KEY,
                    daily_closing_price REAL,
                    percentage_change_1day REAL,
                    percentage_change_30days REAL,
                    percentage_change_365days REAL
                )''')

    # Table for top losers
    c.execute('''CREATE TABLE IF NOT EXISTS myapp_toploser (
                    symbol TEXT PRIMARY KEY,
                    percentage_change_1day REAL
                )''')

    # Table for top gainers
    c.execute('''CREATE TABLE IF NOT EXISTS myapp_topgainer (
                    symbol TEXT PRIMARY KEY,
                    percentage_change_1day REAL
                )''')

    conn.commit()
    conn.close()

def insert_symbol_performance(symbol, daily_closing_price, change_1day, change_30days, change_365days):
    conn = sqlite3.connect('/app/db.sqlite3')
    c = conn.cursor()

    c.execute('''INSERT OR REPLACE INTO myapp_symbolperformance (symbol, daily_closing_price, 
                percentage_change_1day, percentage_change_30days, percentage_change_365days) 
                VALUES (?, ?, ?, ?, ?)''',
              (symbol, daily_closing_price, change_1day, change_30days, change_365days))

    conn.commit()
    conn.close()

def insert_top_losers(symbol, change_1day):

    conn = sqlite3.connect('/app/db.sqlite3')

    c = conn.cursor()

    c.execute('''INSERT OR REPLACE INTO myapp_toploser (symbol, percentage_change_1day) 
                VALUES (?, ?)''',
              (symbol, change_1day))

    conn.commit()
    conn.close()

def insert_top_gainers(symbol, change_1day):
    conn = sqlite3.connect('/app/db.sqlite3')
    c = conn.cursor()

    c.execute('''INSERT OR REPLACE INTO myapp_topgainer (symbol, percentage_change_1day) 
                VALUES (?, ?)''',
              (symbol, change_1day))

    conn.commit()
    conn.close()

def fetch_stock_data(symbol):
    try:
        end_date = datetime.now()
        days_back = 365
        start_date = (end_date - timedelta(days=days_back)).strftime('%Y-%m-%d')

        data = yahooFinance.get_data(symbol, start_date, end_date)
        return data
    except Exception as e:
        print(f"Error fetching data for symbol {symbol}: {e}")
        return None

def store_data(data, symbol):
    if data is None:
        print("No data to store.")
        return

    conn = get_database_connection()
    c = conn.cursor()

    # Correct the CREATE TABLE statement
    c.execute('''CREATE TABLE IF NOT EXISTS stocks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT,
                    date TEXT,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    volume INTEGER
                )''')

    # Clear existing data for the symbol
    c.execute('DELETE FROM stocks WHERE symbol = ?', (symbol,))

    # Insert data into the 'stocks' table
    for index, row in data.iterrows():
        c.execute("INSERT INTO stocks (symbol, date, open, high, low, close, volume) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (symbol, index.date(), row['open'], row['high'], row['low'], row['close'], row['volume']))

    conn.commit()
    conn.close()

def clear_kpi_data():
    conn = sqlite3.connect('/app/db.sqlite3')
    c = conn.cursor()

    # Clear existing KPI data
    c.execute('DELETE FROM myapp_symbolperformance')
    c.execute('DELETE FROM myapp_toploser')
    c.execute('DELETE FROM myapp_topgainer')

    conn.commit()
    conn.close()

def main():
    symbols = [
        "AAPL", "GOOGL", "MSFT", "AMZN", "META", "TSLA", "NFLX", "NVDA", "BABA", "JPM",  # Existing symbols
        "IBM", "INTC", "ORCL", "CSCO", "ADBE", "CRM", "PYPL", "DIS", "PEP", "KO", "PFE", "MRNA", "NKE", "COST", "WMT"
    ]  # Additional symbols to fetch data for

    for symbol in symbols:
        print(f"Processing data for {symbol}")
        data = fetch_stock_data(symbol)
        store_data(data, symbol)
        print(f"Processed data for {symbol}")

    # Clear old data from KPI tables
    clear_kpi_data()

    create_kpi_tables()

    for symbol in symbols:
        display_and_save_kpis(symbol)
    
    # Fetch and store top gainers and losers
    top_gainers, top_losers = fetch_top_gainers_losers(1)

    if top_gainers:
        print("Top Gainers in the last 24 hours:")
        for rank, (symbol, _, change) in enumerate(top_gainers, start=1):
            print(f"Rank {rank}: Symbol: {symbol}, 1-Day Change: {change:.2f}%")
            insert_top_gainers(symbol, change)

    if top_losers:
        print("Top Losers in the last 24 hours:")
        for rank, (symbol, _, change) in enumerate(top_losers, start=1):
            print(f"Rank {rank}: Symbol: {symbol}, 1-Day Change: {change:.2f}%")
            insert_top_losers(symbol, change)

if __name__ == "__main__":
    main()
