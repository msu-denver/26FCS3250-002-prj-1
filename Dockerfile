# GPA Calculator Web App - CS3250 Project 1
#
# Build:  docker build -t gpa-calculator .
# Run:    docker run --rm -p 5000:5000 gpa-calculator
#
# The Flask app resolves templates/ and static/ relative to the repository root
# (two levels above src/app), and Flask-SQLAlchemy puts the SQLite file in
# ./instance relative to the working directory. The layout below mirrors the
# local checkout exactly, and the app is started from /srv/src.

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app

WORKDIR /srv

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /srv/src/
COPY templates/ /srv/templates/
COPY static/ /srv/static/

WORKDIR /srv/src

# Create prj1.db and seed the course catalog (idempotent).
RUN python init_db.py

# Run unprivileged.
RUN useradd --create-home --uid 1000 appuser \
    && chown -R appuser:appuser /srv
USER appuser

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host", "0.0.0.0", "--port", "5000"]
