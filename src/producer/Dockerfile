FROM python:3.10-slim

# Install required dependencies for malware scripts
RUN pip install --no-cache-dir requests

# Security: Run as non-root user
RUN useradd -m -u 1000 producer && \
    mkdir -p /app && \
    chown -R producer:producer /app

WORKDIR /app

# Copy producer scripts
COPY producer.py ./
COPY traffic_generator.py ./
COPY secured_malwares/ ./secured_malwares/

# Switch to non-root user
USER producer

# Run the producer which executes secured malware scripts
# All scripts target internal Docker network only (consumer service)
CMD ["python", "producer.py"]
