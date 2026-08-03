from __future__ import annotations

from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.agency import Agency


class AgencyCRUD:
    @staticmethod
    def get_by_id(session: Session, agency_id: int) -> Agency | None:
        result = session.execute(select(Agency).where(Agency.id == agency_id))
        return result.scalars().first()

    @staticmethod
    def list(session: Session) -> list[Agency]:
        result = session.execute(select(Agency).order_by(Agency.created_at.desc()))
        return list(result.scalars().all())

    @staticmethod
    def create(session: Session, name: str, address: str | None = None) -> Agency:
        agency = Agency(name=name, address=address, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        session.add(agency)
        session.commit()
        session.refresh(agency)
        return agency
