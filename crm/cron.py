import requests
from datetime import datetime

def update_low_stock():

    mutation = '''
    mutation {
        updateLowStockProducts {
            updated
            message
        }
    }
    '''
    response = requests.post('http://localhost:8000/graphql', json={'query': mutation})
    data = response.json()

    with open('/tmp/low_stock_updates_log.txt', 'a') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        updates = data.get('data', {}).get('updateLowStockProducts', {})
        for name in updates.get('updated', []):
            f.write(f"{timestamp} - Updated stock for: {name}\n")


def log_crm_heartbeat():
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    try:
        res = requests.post('http://localhost:8000/graphql', json={'query': '{ hello }'})
        status = 'CRM is alive' if res.status_code == 200 else 'GraphQL down'
    except:
        status = 'GraphQL unreachable'

    with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
        f.write(f"{timestamp} {status}\n")

