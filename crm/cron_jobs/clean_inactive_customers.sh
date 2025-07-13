#!/bin/bash
cd /absolute/path/to/alx-backend-graphql_crm
source venv/bin/activate

python manage.py shell << END
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer
cutoff = timezone.now() - timedelta(days=365)
deleted, _ = Customer.objects.filter(orders__isnull=True, created_at__lt=cutoff).delete()
with open("/tmp/customer_cleanup_log.txt", "a") as f:
    from datetime import datetime
    f.write(f"{datetime.now()} - Deleted {deleted} customers\n")
END

