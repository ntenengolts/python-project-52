install:
	uv pip install -r requirements.lock

collectstatic:
	uv python -- manage.py collectstatic --noinput

migrate:
	uv python -- manage.py migrate

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi
