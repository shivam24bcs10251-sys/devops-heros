FROM python:3.12-slim
WORKDIR /application
COPY app ./app
USER 10001:10001
EXPOSE 8080
CMD ["python", "-m", "app.server"]
