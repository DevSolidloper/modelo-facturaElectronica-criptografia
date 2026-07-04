#!/bin/bash
source .venv/bin/activate
echo "Servidor de la billetera iniciado en http://localhost:8003"
uvicorn app.main:app --port 8003 --reload
