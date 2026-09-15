# --- Base image: Python 3.11 on Debian (ARM64-compatible) ---
FROM python:3.11-slim-bookworm

# --- System dependencies ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# --- Working directory inside the container ---
WORKDIR /app

# --- Install Python deps first (better Docker layer caching) ---
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Copy the project code ---
COPY . .

# --- Data directory for SQLite (mounted from host) ---
RUN mkdir -p /data

# --- Make entrypoint executable ---
RUN chmod +x docker-entrypoint.sh

# --- Expose Flask port ---
EXPOSE 5000

# --- Healthcheck: hit the API every 30s (accept 200 or 401) ---
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/api/dashboard | grep -qE "^(200|401)$" || exit 1

# --- Run the app via entrypoint ---
ENTRYPOINT ["./docker-entrypoint.sh"]