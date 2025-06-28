# syntax=docker/dockerfile:1
FROM python:3.10-slim

# install uv and dependencies
RUN pip install uv

# install project dependencies
COPY requirements.lock /app/requirements.lock
RUN uv pip install -r /app/requirements.lock

# copy code
COPY . /app

# workdir
WORKDIR /app

# expose port
EXPOSE 3000

# default entrypoint
ENTRYPOINT ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:3000"]
