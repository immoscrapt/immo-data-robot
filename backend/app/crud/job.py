from __future__ import annotations

from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.job import Job


class JobCRUD:
    @staticmethod
    def get_by_id(session: Session, job_id: int) -> Job | None:
        result = session.execute(select(Job).where(Job.id == job_id))
        return result.scalars().first()

    @staticmethod
    def list(session: Session) -> list[Job]:
        result = session.execute(select(Job).order_by(Job.created_at.desc()))
        return list(result.scalars().all())

    @staticmethod
    def create(session: Session, name: str, description: str | None = None, payload: str | None = None) -> Job:
        job = Job(name=name, description=description, payload=payload, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        session.add(job)
        session.commit()
        session.refresh(job)
        return job

    @staticmethod
    def update(session: Session, job: Job, status: str | None = None) -> Job:
        if status is not None:
            job.status = status
        job.updated_at = datetime.utcnow()
        session.add(job)
        session.commit()
        session.refresh(job)
        return job
