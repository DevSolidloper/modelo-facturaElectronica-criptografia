#!/bin/bash
source .venv/bin/activate
echo "Servidor de la registraduría iniciado en http://localhost:8000"
uvicorn app.main:app --port 8000 --reload
