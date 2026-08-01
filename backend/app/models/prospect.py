from datetime import datetime
from enum import Enum
from sqlalchemy import String, Integer, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ProspectStatus(str, Enum):
    nouveau = "Nouveau"
    contacte = "Contacté"
    rdv = "RDV"
    mandat = "Mandat"
    clos = "Clos"


class Prospect(Base):
    __tablename__ = "prospects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    agency_id: Mapped[int] = mapped_column(Integer, nullable=False)
    owner_name: Mapped[str] = mapped_column(String(255), nullable=False)
    property_address: Mapped[str] = mapped_column(String(512), nullable=False)
    city: Mapped[str] = mapped_column(String(128), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=False)
    surface: Mapped[float] = mapped_column(Float, nullable=True)
    estimated_value: Mapped[float] = mapped_column(Float, nullable=True)
    status: Mapped[ProspectStatus] = mapped_column(String(50), nullable=False, default=ProspectStatus.nouveau.value)
    score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    agency = relationship("Agency", backref="prospects", lazy="selectin")
