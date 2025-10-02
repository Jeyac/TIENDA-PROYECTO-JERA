PY=python
PIP=pip

install:
	$(PIP) install -r requirements.txt

run:
	$(PY) app.py

migrate-init:
	$(PY) -c "from app import create_app, db; from flask_migrate import init; app=create_app();\nimport os;\nwith app.app_context():\n    init(directory='migrations')"

migrate:
	$(PY) -c "from app import create_app, db; from flask_migrate import migrate; app=create_app();\nwith app.app_context(): migrate()"

upgrade:
	$(PY) -c "from app import create_app, db; from flask_migrate import upgrade; app=create_app();\nwith app.app_context(): upgrade()"

test:
	pytest --cov=.

seed-admin:
	$(PY) seed_admin.py

setup: install migrate-init migrate upgrade seed-admin
	@echo "✅ Setup completo: dependencias, migraciones y usuario admin creados"

clean:
	rm -rf migrations/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	find . -name "*.pyc" -delete


