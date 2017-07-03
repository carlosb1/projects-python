from celery.schedules import crontab
from datetime import timedelta

CELERY_BROKER_URL="amqp://guest@localhost//"
CELERYBEAT_SCHEDULE = {
	'every-day': {
		'task': 'forecast.search_spot',
                'schedule': timedelta(days=1),
	}
}
CELERY_TIMEZONE='UTC'
