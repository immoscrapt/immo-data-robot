from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.crud.execution import ExecutionCRUD
from app.crud.job import JobCRUD
from app.db.session import get_async_session
from app.models.user import User
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/", response_model=list[dict])
def list_jobs(
    session: Session = Depends(get_async_session),
    user: User = Depends(get_current_user),
):
    jobs = JobCRUD.list(session)
    return [{"id": job.id, "name": job.name, "status": job.status} for job in jobs]


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_job(
    payload: dict[str, str],
    session: Session = Depends(get_async_session),
    user: User = Depends(get_current_user),
):
    job = JobCRUD.create(session, name=payload.get("name", "job"), description=payload.get("description"), payload=str(payload))
    return {"id": job.id, "name": job.name, "status": job.status}


@router.get("/history")
def execution_history(
    session: Session = Depends(get_async_session),
    user: User = Depends(get_current_user),
):
    executions = ExecutionCRUD.list(session)
    return [{"id": execution.id, "connector": execution.connector, "status": execution.status} for execution in executions]
