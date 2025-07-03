install:
	uv sync

collectstatic:
	uv run python manage.py collectstatic --noinput

migrate:
	uv run python manage.py migrate

test:
	uv run pytest -vv

build:
	./build.sh

render-start:
	uv run gunicorn task_manager.wsgi

start:
	uv run manage.py runserver 0.0.0.0:8000

format:
	black .
