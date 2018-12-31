export FLASK_RUN_PORT=5002
export FLASK_APP=run.py
#flask run & >> backend.log
gunicorn app:app -b 0.0.0.0:5002 & >> backend.log
celery -A tasks worker --loglevel=info
cd frontend && npm run dev & >> frontend.log

