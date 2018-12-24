export FLASK_RUN_PORT=5002
export FLASK_APP=run.py
flask run & >> backend.log
cd frontend && npm run dev & >> frontend.log

