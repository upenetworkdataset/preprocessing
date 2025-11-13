FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir pandas pyarrow
CMD ["python", "logger.py"]
