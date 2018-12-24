export FLASK_RUN_PORT=5002
export FLASK_APP=run.py
#flask run & >> backend.log
gunicorn run:app -b 0.0.0.0:5002 & >> backend.log
cd frontend && npm run dev & >> frontend.log

