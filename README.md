# Limpeza360

SaaS multi-tenant para gestão de limpeza, higienização e lavanderia.

## Executar

```bash
cp .env.example .env
docker compose up -d --build
```

- Frontend: http://localhost:5173
- API Swagger: http://localhost:8000/docs
- Login dev: `admin@limpeza360.local` / `Admin123!`

## Comandos locais

```bash
npm run build
PYTHONPATH=backend pytest -q backend/app/tests
python3 -m pip install -r backend/requirements.txt
```

## Arquitetura

- Backend: FastAPI, SQLAlchemy, Alembic, JWT HMAC, RBAC, auditoria e isolamento por `tenant_id`.
- Banco: PostgreSQL via Docker Compose.
- Frontend: HTML/CSS/JS sem dependências externas por causa do bloqueio 403 do registry NPM no ambiente.
- Seed: `npm run seed` popula dados de desenvolvimento separados.
