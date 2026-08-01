# IMMO DATA ROBOT

Plateforme SaaS B2B conçue pour les agences immobilières.

## Objectif

Aider les agences à identifier, qualifier et suivre les meilleures opportunités de prospection immobilière.

## Technologie

- Frontend : Next.js 15, React, TypeScript, Tailwind CSS, shadcn/ui, TanStack Query, React Hook Form, Zod
- Backend : Python 3.12, FastAPI, SQLAlchemy 2, Alembic, Pydantic v2, JWT, Argon2
- Base de données : PostgreSQL
- Infrastructure : Docker, Docker Compose
- Tests : Pytest, Playwright, Vitest
- CI/CD : GitHub Actions

## Structure

- `backend/` : API FastAPI, modèle de domaine, services, routes
- `frontend/` : interface Next.js
- `docker-compose.yml` : orchestration locale
- `.env.example` : variables d'environnement de base

## Installation

1. Copier `.env.example` en `.env`
2. Compléter les variables d'environnement
3. Lancer `docker compose up --build`

## Services

- API : http://localhost:8000
- Frontend : http://localhost:3000

## Développement

- Backend :

```bash
cd backend
uvicorn app.main:app --reload
```

- Frontend :

```bash
cd frontend
npm install
npm run dev
```

## Statut

🚧 En développement