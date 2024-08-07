import sqlite3
import yahoo_fin.stock_info as yahooFinance
from datetime import datetime, timedelta


DB_PATH = '/app/db.sqlite3'


def get_database_connection():
  return sqlite3.connect(DB_PATH)


def fetch_daily_closing_price(symbol):
  with get_database_connection() as conn:
      c = conn.cursor()
      query = """
      SELECT date, close
      FROM stocks
      WHERE symbol = ?
      ORDER BY date DESC
      LIMIT 1
      """
      c.execute(query, (symbol,))
      return c.fetchone()


def fetch_latest_trading_day(symbol):
  with get_database_connection() as conn:
      c = conn.cursor()
      query = """
      SELECT date
      FROM stocks
      WHERE symbol = ?
      ORDER BY date DESC
      LIMIT 1
      """
      c.execute(query, (symbol,))
      result = c.fetchone()
      return result[0] if result else None


def fetch_previous_trading_day(symbol, current_date):
  with get_database_connection() as conn:
      c = conn.cursor()
      query = """
      SELECT date
      FROM stocks
      WHERE symbol = ?
        AND date < ?
      ORDER BY date DESC
      LIMIT 1
      """
      c.execute(query, (symbol, current_date))
      result = c.fetchone()
      return result[0] if result else None


def fetch_nearest_trading_day(symbol, target_date):
  with get_database_connection() as conn:
      c = conn.cursor()
      query = """
      SELECT date
      FROM stocks
      WHERE symbol = ?
        AND date BETWEEN ? AND ?
      ORDER BY date ASC
      LIMIT 1
      """
      c.execute(query, (symbol, (target_date - timedelta(days=7)).strftime('%Y-%m-%d'), (target_date + timedelta(days=7)).strftime('%Y-%m-%d')))
      result = c.fetchone()
      return result[0] if result else None


def fetch_price_change_percentage(symbol, days):
  with get_database_connection() as conn:
      c = conn.cursor()


      # Fetch the last date available in the stocks table for the given symbol
      end_date = fetch_latest_trading_day(symbol)


      if not end_date:
          return None


      end_date = datetime.strptime(end_date, '%Y-%m-%d')


      # Fetch the nearest available trading day that is 'days' ago
      target_start_date = end_date - timedelta(days=days)
      start_date = fetch_nearest_trading_day(symbol, target_start_date)


      if not start_date:
          return None


      query = """
      SELECT (SELECT close FROM stocks
              WHERE symbol = ? AND date = ?) AS start_price,
             (SELECT close FROM stocks
              WHERE symbol = ? AND date = ?) AS end_price
      """
      c.execute(query, (symbol, start_date, symbol, end_date.strftime('%Y-%m-%d')))
      result = c.fetchone()


      if result and result[0] and result[1]:
          start_price, end_price = result
          return ((end_price - start_price) / start_price) * 100
      return None


def fetch_top_gainers_losers():
  with get_database_connection() as conn:
      c = conn.cursor()
      query = """
      SELECT symbol, percentage_change_1day
      FROM myapp_symbolperformance
      ORDER BY percentage_change_1day DESC
      """
      c.execute(query)
      results = c.fetchall()


      if results:
          top_gainers = results[:5]  # Top 5 gainers
          top_losers = results[-5:]  # Top 5 losers
          return top_gainers, top_losers
      return None, None


def display_and_save_kpis(symbol):
  print(f"KPIs for {symbol}:")
  closing_price = fetch_daily_closing_price(symbol)
  if closing_price:
      daily_closing_price = closing_price[1]
      print(f"Daily Closing Price: {daily_closing_price} on {closing_price[0]}")
  else:
      daily_closing_price = None


  change_1day = fetch_price_change_percentage(symbol, 1)
  change_30days = fetch_price_change_percentage(symbol, 30)
  change_365days = fetch_price_change_percentage(symbol, 365)


  print(f"Changes for {symbol}: 1 day: {change_1day}, 30 days: {change_30days}, 365 days: {change_365days}")


  if change_1day is not None and change_30days is not None and change_365days is not None:
      insert_symbol_performance(symbol, daily_closing_price, change_1day, change_30days, change_365days)


def create_kpi_tables():
  with get_database_connection() as conn:
      c = conn.cursor()


      c.execute('''CREATE TABLE IF NOT EXISTS myapp_symbolperformance (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      symbol TEXT,
                      daily_closing_price REAL,
                      percentage_change_1day REAL,
                      percentage_change_30days REAL,
                      percentage_change_365days REAL
                  )''')


      c.execute('''CREATE TABLE IF NOT EXISTS myapp_toploser (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      symbol TEXT,
                      percentage_change_1day REAL
                  )''')


      c.execute('''CREATE TABLE IF NOT EXISTS myapp_topgainer (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      symbol TEXT,
                      percentage_change_1day REAL
                  )''')


def insert_symbol_performance(symbol, daily_closing_price, change_1day, change_30days, change_365days):
  with get_database_connection() as conn:
      c = conn.cursor()
      try:
          c.execute('''INSERT OR REPLACE INTO myapp_symbolperformance (symbol, daily_closing_price,
                      percentage_change_1day, percentage_change_30days, percentage_change_365days)
                      VALUES (?, ?, ?, ?, ?)''',
                    (symbol, daily_closing_price, change_1day, change_30days, change_365days))
          print(f"Inserted {symbol} performance successfully")
      except Exception as e:
          print(f"Error inserting {symbol} performance: {e}")


def insert_top_losers(symbol, change_1day):
  with get_database_connection() as conn:
      c = conn.cursor()
      c.execute('''INSERT OR REPLACE INTO myapp_toploser (symbol, percentage_change_1day)
                  VALUES (?, ?)''',
                (symbol, change_1day))


def insert_top_gainers(symbol, change_1day):
  with get_database_connection() as conn:
      c = conn.cursor()
      c.execute('''INSERT OR REPLACE INTO myapp_topgainer (symbol, percentage_change_1day)
                  VALUES (?, ?)''',
                (symbol, change_1day))


def fetch_stock_data(symbol):
  try:
      end_date = datetime.now()
      start_date = (end_date - timedelta(days=365)).strftime('%Y-%m-%d')
      return yahooFinance.get_data(symbol, start_date, end_date)
  except Exception as e:
      print(f"Error fetching data for symbol {symbol}: {e}")
      return None


def store_data(data, symbol):
  if data is None:
      print("No data to store.")
      return


  with get_database_connection() as conn:
      c = conn.cursor()


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


def clear_kpi_data():
  with get_database_connection() as conn:
      c = conn.cursor()
      c.execute('DELETE FROM myapp_symbolperformance')
      c.execute('DELETE FROM myapp_toploser')
      c.execute('DELETE FROM myapp_topgainer')


def main():
  symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "META", "TSLA", "NFLX", "NVDA", "BABA", "JPM"]


  for symbol in symbols:
      print(f"Processing data for {symbol}")
      data = fetch_stock_data(symbol)
      store_data(data, symbol)
      print(f"Processed data for {symbol}")


  clear_kpi_data()
  create_kpi_tables()


  for symbol in symbols:
      display_and_save_kpis(symbol)


  top_gainers, top_losers = fetch_top_gainers_losers()


  if top_gainers:
      print("Top Gainers in the last 24 hours:")
      for rank, (symbol, change) in enumerate(top_gainers, start=1):
          print(f"Rank {rank}: Symbol: {symbol}, 1-Day Change: {change:.2f}%")
          insert_top_gainers(symbol, change)


  if top_losers:
      print("Top Losers in the last 24 hours:")
      for rank, (symbol, change) in enumerate(top_losers, start=1):
          print(f"Rank {rank}: Symbol: {symbol}, 1-Day Change: {change:.2f}%")
          insert_top_losers(symbol, change)


if __name__ == "__main__":
  main()


