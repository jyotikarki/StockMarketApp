import os
import sys
import django
from prometheus_client import Gauge, generate_latest
from django.db import connection
from django.http import HttpResponse

# Add the myproject directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

# Define custom metrics
gauge = Gauge('percentage_change_1day', 'Percentage change in stock price over 1 day', ['stock_symbol'])

def fetch_stock_data():
    with connection.cursor() as cursor:
        query = 'SELECT symbol, percentage_change_1day FROM myapp_symbolperformance'
        cursor.execute(query)
        stock_data = cursor.fetchall()
    print("Fetched stock data:", stock_data)  # Debug print
    return [{'symbol': row[0], 'percentage_change_1day': row[1]} for row in stock_data]

def update_metrics():
    stock_data = fetch_stock_data()
    for stock in stock_data:
        gauge.labels(stock_symbol=stock['symbol']).set(stock['percentage_change_1day'])
    print("Updated metrics")  # Debug print

# if __name__ == '__main__':
#     update_metrics()

def new_metrics(request):
    update_metrics()
    return HttpResponse(generate_latest(), content_type='text/plain; version=0.0.4; charset=utf-8')