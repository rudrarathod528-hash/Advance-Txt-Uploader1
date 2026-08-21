FROM python:3.12-slim

WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        libffi-dev \
        ffmpeg \
        aria2 \
        make \
        cmake \
        wget \
        unzip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Build Bento4 / mp4decrypt
RUN wget -q https://github.com/axiomatic-systems/Bento4/archive/v1.6.0-639.zip && \
    unzip v1.6.0-639.zip && \
    cd Bento4-1.6.0-639 && \
    mkdir build && \
    cd build && \
    cmake -DCMAKE_CXX_STANDARD=17 .. && \
    make -j$(nproc) && \
    cp mp4decrypt /usr/local/bin/ && \
    cd /app && \
    rm -rf Bento4-1.6.0-639 v1.6.0-639.zip

# Copy project
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install -U yt-dlp && \
    pip install --no-cache-dir m3u8 aiofiles aiohttp gunicorn

# Make N_m3u8DL-RE executable
RUN chmod +x /app/modules/N_m3u8DL-RE

# aria2 configuration
RUN mkdir -p /root/.aria2 && \
    printf '%s\n' \
    'max-connection-per-server=16' \
    'min-split-size=1M' \
    'split=16' \
    'max-concurrent-downloads=32' \
    'file-allocation=none' \
    'retry-wait=2' \
    'max-tries=5' \
    'timeout=30' \
    'connect-timeout=10' \
    > /root/.aria2/aria2.conf

ENV COOKIES_FILE_PATH=/app/modules/youtube_cookies.txt

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-8000} app:app & python3 modules/main.py"]
