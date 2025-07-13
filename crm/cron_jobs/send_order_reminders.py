from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta

transport = RequestsHTTPTransport(url='http://localhost:8000/graphql', verify=True, retries=3)
client = Client(transport=transport, fetch_schema_from_transport=True)

seven_days_ago = (datetime.now() - timedelta(days=7)).date()
query = gql('''
    query GetRecentOrders($date: Date!) {
        orders(orderDate_Gte: $date) {
            id
            customer {
                email
            }
        }
    }
''')

params = {"date": str(seven_days_ago)}
response = client.execute(query, variable_values=params)

with open("/tmp/order_reminders_log.txt", "a") as f:
    for order in response.get("orders", []):
        f.write(f"{datetime.now()} - Order {order['id']} for {order['customer']['email']}\n")

print("Order reminders processed!")
