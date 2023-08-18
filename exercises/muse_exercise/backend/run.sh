export DEMO_SILENT_CFG=docker.cfg 
pipenv run  python start_celery.py &
pipenv run gunicorn app:app -w 4 --threads 12 -b 0.0.0.0:5002 --log-level=debug 
