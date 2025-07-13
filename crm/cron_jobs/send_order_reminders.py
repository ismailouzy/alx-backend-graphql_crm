import requests
from datetime import datetime, timedelta

query = '''
query {
  orders(orderDate_Gte: "%s") {
    id
    customer {
      email
    }
  }
}
''' % (datetime.now() - timedelta(days=7)).date()

response = requests.post('http://localhost:8000/graphql', json={'query': query})
data = response.json()

with open("/tmp/order_reminders_log.txt", "a") as f:
    for order in data.get('data', {}).get('orders', []):
        f.write(f"{datetime.now()} - Order {order['id']} for {order['customer']['email']}\n")

print("Order reminders processed!")
