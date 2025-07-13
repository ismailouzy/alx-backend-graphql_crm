from celery import shared_task
from datetime import datetime
import requests

@shared_task
def generate_crm_report():
    query = '''
    query {
        customers { id }
        orders { id totalamount }
    }
    '''
    res = requests.post("http://localhost:8000/graphql", json={"query": query})
    data = res.json().get("data", {})
    num_customers = len(data.get("customers", []))
    orders = data.get("orders", [])
    total_orders = len(orders)
    revenue = sum(float(o['totalamount']) for o in orders)
    
    with open("/tmp/crm_report_log.txt", "a") as f:
        f.write(f"{datetime.now()} - Report: {num_customers} customers, {total_orders} orders, {revenue} revenue\n")
