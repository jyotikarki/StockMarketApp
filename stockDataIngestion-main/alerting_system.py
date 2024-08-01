import sqlite3
import pandas as pd
import smtplib
from email.mime.text import MIMEText

# Function to send email alerts
def send_alert(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'your_email@example.com'
    msg['To'] = 'recipient@example.com'

    with smtplib.SMTP('smtp.example.com') as server:
        server.login('your_email@example.com', 'your_password')
        server.send_message(msg)

def check_alerts():
    conn = sqlite3.connect('stocks.db')
    query = '''
    SELECT symbol, date, close 
    FROM stocks
    WHERE date = (SELECT MAX(date) FROM stocks WHERE symbol = stocks.symbol)
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()

    threshold = 0.10  # 10% change
    alerts = []

    for symbol in df['symbol'].unique():
        symbol_data = df[df['symbol'] == symbol]
        recent_close = symbol_data['close'].values[0]

        # Example check for change (you might need to adjust based on your logic)
        if recent_close < previous_close * (1 - threshold) or recent_close > previous_close * (1 + threshold):
            alerts.append(f"{symbol} has significant price change: {recent_close}")

    if alerts:
        send_alert('Stock Price Alerts', '\n'.join(alerts))

if __name__ == '__main__':
    check_alerts()
