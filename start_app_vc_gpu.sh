#!/bin/bash

# Start the app
HF_ENDPOINT=https://hf-mirror.com python3 -m src.main --certfile cf.pem --keyfile cf.key --port 20000 --llm-type ollama --tts-type xtts-v2 --vad-type pyannote --vad-args '{"auth_token": "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"}'

#python -m gunicorn --bind 0.0.0.0:8765  --workers 1 --reload --timeout 0 --keyfile /etc/letsencrypt/live/${SSL_DOMAIN_NAME}/privkey.pem --certfile /etc/letsencrypt/live/${SSL_DOMAIN_NAME}/cert.pem src.main -k uvicorn.workers.UvicornWorker
