#!/bin/bash
source .venv/bin/activate
echo "Servidor de la DIAN iniciado en http://localhost:8002"
uvicorn app.main:app --port 8002 --reload
