FROM python:3.12-slim
LABEL org.opencontainers.image.source="https://github.com/shivam24bcs10251-sys/devops-heros"
WORKDIR /application
COPY requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade pip && python -m pip install --no-cache-dir -r requirements.txt && python -m pip uninstall -y pip setuptools
COPY app ./app
USER 10001:10001
EXPOSE 5001
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "2", "app.app:app"]
