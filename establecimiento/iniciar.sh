#!/bin/bash
source .venv/bin/activate
echo "Servidor del establecimiento iniciado en http://localhost:8001"
uvicorn app.main:app --port 8001 --reload
