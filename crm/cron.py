from datetime import datetime
from gql.transport.requests import RequestsHTTPTransport
from gql import gql, Client

def log_crm_heartbeat():
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    try:
        transport = RequestsHTTPTransport(url='http://localhost:8000/graphql', verify=True, retries=3)
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql("query { hello }")
        res = client.execute(query)
        status = 'CRM is alive' if res.get('hello') else 'GraphQL empty response'
    except Exception:
        status = 'GraphQL unreachable'

    with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
        f.write(f"{timestamp} {status}\n")

def update_low_stock():
    from datetime import datetime
    transport = RequestsHTTPTransport(url='http://localhost:8000/graphql', verify=True, retries=3)
    client = Client(transport=transport, fetch_schema_from_transport=True)

    mutation = gql('''
    mutation {
        updateLowStockProducts {
            updated
            message
        }
    }
    ''')

    response = client.execute(mutation)

    with open('/tmp/low_stock_updates_log.txt', 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        updates = response.get('updateLowStockProducts', {})
        for name in updates.get('updated', []):
            f.write(f"{timestamp} - Updated stock for: {name}\n")

