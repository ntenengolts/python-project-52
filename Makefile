install:
	uv pip install -r requirements.lock

collectstatic:
	uv run python manage.py collectstatic --noinput

migrate:
	uv run python manage.py migrate

build:
	./build.sh

render-start:
	uv run gunicorn task_manager.wsgi

format:
	black .

start-server:
	uv run python manage.py runserver 0.0.0.0.3000
