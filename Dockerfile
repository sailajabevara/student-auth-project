# ===============================
# Stage 1: Builder
# ===============================
FROM python:3.11-slim AS builder

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# ===============================
# Stage 2: Runtime
# ===============================
FROM python:3.11-slim

# Set timezone to UTC
ENV TZ=UTC
WORKDIR /app

# Install cron and timezone data
RUN apt-get update && apt-get install -y cron tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy your application code
COPY app ./app
COPY scripts ./scripts
COPY cron ./cron

# Copy key files
COPY student_private.pem .
COPY student_public.pem .
COPY instructor_public.pem .

# Create volume mount points
RUN mkdir -p /data /cron && chmod 755 /data /cron

# Install cron job
RUN chmod 0644 cron/2fa-cron && crontab cron/2fa-cron

# Expose API port
EXPOSE 8080

# Start cron and FastAPI together
CMD ["sh", "-c", "cron && uvicorn app.main:app --host 0.0.0.0 --port 8080"]
