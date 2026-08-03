from __future__ import annotations

from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.execution import Execution


class ExecutionCRUD:
    @staticmethod
    def create(session: Session, connector: str, status: str = "pending", result: str | None = None, job_id: int | None = None) -> Execution:
        execution = Execution(
            job_id=job_id,
            connector=connector,
            status=status,
            result=result,
            started_at=datetime.utcnow(),
            finished_at=None,
        )
        session.add(execution)
        session.commit()
        session.refresh(execution)
        return execution

    @staticmethod
    def list(session: Session) -> list[Execution]:
        result = session.execute(select(Execution).order_by(Execution.started_at.desc().nullslast()))
        return list(result.scalars().all())

    @staticmethod
    def update(session: Session, execution: Execution, status: str | None = None, result: str | None = None) -> Execution:
        if status is not None:
            execution.status = status
        if result is not None:
            execution.result = result
        execution.finished_at = datetime.utcnow()
        session.add(execution)
        session.commit()
        session.refresh(execution)
        return execution
