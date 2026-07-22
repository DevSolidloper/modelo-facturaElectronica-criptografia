#!/bin/bash
cd "$(dirname "$0")"
ROOT="$(pwd)"

echo "Deteniendo procesos previos en los puertos 8000-8003 (si existen)..."
for port in 8000 8001 8002 8003; do
  pid=$(lsof -ti tcp:$port)
  if [ -n "$pid" ]; then
    kill -9 $pid
  fi
done

echo "Iniciando Registraduria en :8000..."
( cd "$ROOT/registraduria" && source ../.venv/bin/activate && PYTHONPATH=".:$ROOT/shared" nohup uvicorn app.main:app --port 8000 > /tmp/registraduria.log 2>&1 & )

echo "Iniciando Establecimiento en :8001..."
( cd "$ROOT/establecimiento" && source ../.venv/bin/activate && PYTHONPATH=".:$ROOT/shared" nohup uvicorn app.main:app --port 8001 > /tmp/establecimiento.log 2>&1 & )

echo "Iniciando DIAN en :8002..."
( cd "$ROOT/dian" && source ../.venv/bin/activate && PYTHONPATH=".:$ROOT/shared" nohup uvicorn app.main:app --port 8002 > /tmp/dian.log 2>&1 & )

echo "Iniciando Wallet en :8003..."
( cd "$ROOT/wallet" && source ../.venv/bin/activate && PYTHONPATH=".:$ROOT/shared" nohup uvicorn app.main:app --port 8003 > /tmp/wallet.log 2>&1 & )

sleep 2

echo ""
echo "Verificando servicios..."
curl -s -o /dev/null -w "Registraduria   (8000): %{http_code}\n" http://localhost:8000/
curl -s -o /dev/null -w "Establecimiento (8001): %{http_code}\n" http://localhost:8001/public-key
curl -s -o /dev/null -w "DIAN            (8002): %{http_code}\n" http://localhost:8002/public-key
curl -s -o /dev/null -w "Wallet          (8003): %{http_code}\n" http://localhost:8003/me

echo ""
echo "Abriendo el dashboard..."
open "$ROOT/dashboard.html"
