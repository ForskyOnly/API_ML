#!/bin/bash
export $(grep -v '^#' .env | xargs)
uvicorn api.app.main:app --host 0.0.0.0 --port 8000