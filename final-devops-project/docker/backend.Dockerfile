FROM python:3.12-alpine
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY application/backend/requirements.txt .
RUN apk upgrade --no-cache && pip install --no-cache-dir -r requirements.txt && \
    addgroup -g 10001 app && adduser -D -u 10001 -G app app && \
    rm -rf /usr/local/lib/python3.12/site-packages/pip* /usr/local/lib/python3.12/site-packages/setuptools*
COPY application/backend/ ./
USER 10001:10001
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
