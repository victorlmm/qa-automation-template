# Runs the suite in an identical environment on any machine.
#   docker build -t qa-tests .
#   docker run --rm -e TEST_ENV=staging -v "$PWD/reports:/app/reports" qa-tests -m smoke
FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && playwright install --with-deps chromium

COPY . .

ENTRYPOINT ["pytest"]
CMD ["-m", "smoke"]
