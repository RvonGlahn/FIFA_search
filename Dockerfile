FROM python:3.8-buster
LABEL authors="Rasmus von Glahn"

# Upgrade pip and install poetry
RUN pip install --upgrade pip && pip install poetry

WORKDIR /api

# Copy only requirements to cache them in docker layer
COPY poetry.lock pyproject.toml /api/

# Project initialization: disable crearing a virtual environment
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --no-dev

# Creating folders, and files for a project:
COPY . /api

RUN python3 api.py

EXPOSE 5000

CMD ["flask", "run", "--port=5000", "--host=0.0.0.0"]
