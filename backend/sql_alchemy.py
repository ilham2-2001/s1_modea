import enum
import os
# Both spellings are bound on purpose. Generated code uses the trailing-
# underscore aliases so a modelled class named List, Optional or DateTime
# cannot shadow them. The PLAIN names are imported too because this file is
# routinely edited afterwards by an LLM, which writes ordinary Python and has
# no reason to know about the aliasing convention; without the plain names
# such edits fail to import:
#
#     Mapped_[Optional[int]]        undefined name 'Optional'
#     mapped_column(DateTime())     undefined name 'DateTime'
#
# so every aliased name below is bound both ways.
from typing import List, Optional, List as List_, Optional as Optional_
from sqlalchemy import (
    create_engine, Enum, UniqueConstraint as _UniqueConstraint, event as _sa_event,
    Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, Interval,
    PickleType, String, Table, Text, Time,
    Column as Column_, ForeignKey as ForeignKey_, Table as Table_,
    Text as Text_, Boolean as Boolean_, String as String_, Date as Date_,
    Time as Time_, DateTime as DateTime_, Float as Float_, Integer as Integer_,
    Interval as Interval_, PickleType as PickleType_,
)
from sqlalchemy.orm import (
    column_property, DeclarativeBase, Mapped, Mapped as Mapped_, mapped_column,
    relationship
)
from datetime import datetime as dt_datetime, time as dt_time, date as dt_date, timedelta as dt_timedelta
from uuid import uuid4 as _uuid4


def _new_str_id() -> str:
    """Server-side surrogate for string primary keys named ``id``.

    A string PK has no autoincrement; without a default every INSERT dies
    on NOT NULL (the id is in nobody's hands: create schemas rightly
    exclude the server-owned ``id``, so the server must mint it).
    """
    return _uuid4().hex


def _configure_sqlite_engine(engine):
    """Enforce declared foreign keys on every SQLite connection."""
    if engine.dialect.name == "sqlite":
        @_sa_event.listens_for(engine, "connect")
        def _enable_foreign_keys(connection, _record):
            previous_autocommit = getattr(connection, "autocommit", None)
            if previous_autocommit is not None:
                connection.autocommit = True
            cursor = connection.cursor()
            try:
                cursor.execute("PRAGMA foreign_keys=ON")
            finally:
                cursor.close()
                if previous_autocommit is not None:
                    connection.autocommit = previous_autocommit


class Base(DeclarativeBase):
    pass

# Definitions of Enumerations
class TimeOffStatus(enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"


# Tables definition for many-to-many relationships

# Tables definition
class TimeOffRequest(Base):
    __tablename__ = "timeoffrequest"
    id: Mapped_[int] = mapped_column(Integer_, primary_key=True)
    startDate: Mapped_[dt_date] = mapped_column(Date_)
    endDate: Mapped_[dt_date] = mapped_column(Date_)
    reason: Mapped_[str] = mapped_column(String_(100))
    submittedAt: Mapped_[dt_datetime] = mapped_column(DateTime_)
    approvedAt: Mapped_[Optional_[dt_datetime]] = mapped_column(DateTime_, nullable=True)
    status: Mapped_[TimeOffStatus] = mapped_column(Enum(TimeOffStatus))
    approvedBy_id: Mapped_[int] = mapped_column(ForeignKey_("manager.id"), nullable=True)
    requester_id: Mapped_[int] = mapped_column(ForeignKey_("employee.id"))

class Employee(Base):
    __tablename__ = "employee"
    id: Mapped_[int] = mapped_column(Integer_, primary_key=True)
    name: Mapped_[str] = mapped_column(String_(100))
    email: Mapped_[str] = mapped_column(String_(100))
    hiredDate: Mapped_[dt_date] = mapped_column(Date_)
    position: Mapped_[str] = mapped_column(String_(100))
    manager_id: Mapped_[int] = mapped_column(ForeignKey_("manager.id"), nullable=True)
    type_spec: Mapped_[str] = mapped_column(String_(50))
    __mapper_args__ = {
        "polymorphic_identity": "employee",
        "polymorphic_on": "type_spec",
    }

class Manager(Employee):
    __tablename__ = "manager"
    id: Mapped_[int] = mapped_column(ForeignKey_("employee.id"), primary_key=True)
    department: Mapped_[str] = mapped_column(String_(100))
    __mapper_args__ = {
        "polymorphic_identity": "manager",
    }


#--- Relationships of the timeoffrequest table

TimeOffRequest.approvedBy: Mapped_["Manager"] = relationship("Manager", back_populates="approvedRequests", uselist=False, foreign_keys=[TimeOffRequest.approvedBy_id])

TimeOffRequest.requester: Mapped_["Employee"] = relationship("Employee", back_populates="timeOffRequests", uselist=False, foreign_keys=[TimeOffRequest.requester_id])

#--- Relationships of the employee table

Employee.manager: Mapped_["Manager"] = relationship("Manager", back_populates="teamMembers", uselist=False, foreign_keys=[Employee.manager_id])
Employee.timeOffRequests: Mapped_[List_["TimeOffRequest"]] = relationship("TimeOffRequest", back_populates="requester", foreign_keys=[TimeOffRequest.requester_id])

#--- Relationships of the manager table
Manager.approvedRequests: Mapped_[List_["TimeOffRequest"]] = relationship("TimeOffRequest", back_populates="approvedBy", foreign_keys=[TimeOffRequest.approvedBy_id])
Manager.teamMembers: Mapped_[List_["Employee"]] = relationship("Employee", back_populates="manager", foreign_keys=[Employee.manager_id])

# Database connection (override the default with the DATABASE_URL environment variable)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/Class_Diagram.db")  # SQLite connection
engine = create_engine(DATABASE_URL)
_configure_sqlite_engine(engine)

if __name__ == "__main__":
    # Create tables in the database only when this module is executed directly,
    # so importing it never touches the database as a side effect.
    if DATABASE_URL.startswith("sqlite"):
        os.makedirs("data", exist_ok=True)  # folder for the default SQLite database
    Base.metadata.create_all(engine, checkfirst=True)