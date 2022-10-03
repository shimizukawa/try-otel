docker compose up --no-start
pip install -r backend/requirements.txt -c constraints.txt
pip install -r console/requirements.txt -c constraints.txt
(cd frontend && npm install)
