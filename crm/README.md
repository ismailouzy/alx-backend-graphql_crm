# CRM Background Tasks Setup

## Redis Install
sudo apt install redis-server

## Migrations
python manage.py migrate

## Start Celery
celery -A crm worker -l info

## Start Celery Beat
celery -A crm beat -l info

## Logs
/tmp/crm_report_log.txt

