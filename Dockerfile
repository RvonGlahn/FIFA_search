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

# RUN cp .env.default .envenvironemnt vENVIRON

EXPOSE 5000

CMD ["flask", "run", "--port=5000", "--host=0.0.0.0"]
# CMD ["gunicorn", "--bind 0.0.0.0:5000", "wsgi:app"]
# CMD ["python3", "app.py" ]