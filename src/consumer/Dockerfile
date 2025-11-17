FROM python:3.10-slim

# Security: Run as non-root user
RUN useradd -m -u 1000 consumer && \
    mkdir -p /app && \
    chown -R consumer:consumer /app

WORKDIR /app

# Copy only necessary files
COPY consumer.py .

# Switch to non-root user
USER consumer

# No external dependencies needed - uses only Python stdlib
CMD ["python", "consumer.py"]
