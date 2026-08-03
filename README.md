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
- `robot/` : automation engine modulaire avec browser, core, connectors, sessions, screenshots
- `docker-compose.yml` : orchestration locale
- `.env.example` : variables d'environnement de base

## Sprint 1 - Automation Engine

Le sprint 1 met en place un moteur d'automatisation professionnel avec :

- `BrowserManager` pour gérer le cycle de vie du navigateur
- `SessionManager` pour persister les sessions d'exécution
- `RetryManager` pour maîtriser les échecs temporaires
- `Logger` pour journaliser les opérations
- `ScreenshotManager` pour capturer les artefacts de run
- une architecture modulaire prête pour les connecteurs Cadastre, DVF, Pappers, LinkedIn et Lusha

## Installation

1. Copier `.env.example` en `.env`
2. Compléter les variables d'environnement
3. Exécuter `./bootstrap.sh`
4. Ou lancer `make install && docker compose up --build`

## Services

- API : http://localhost:8000
- Frontend : http://localhost:3000

## Développement

- Bootstrap local complet :

```bash
./bootstrap.sh
```

- Backend :

```bash
cd backend
uvicorn app.main:app --reload
```

- Robot :

```bash
cd robot
python main.py
```

- Frontend :

```bash
cd frontend
npm install
npm run dev
```

## Statut

🚧 En développement