"""
User model + Role enum.

Design choice: roles are a fixed Python enum (Student/Recruiter/
PlacementOfficer) stored as a string column on User, rather than a
separate `roles` table joined many-to-many. The original spec listed
`users` and `roles` as separate tables — that's the right design if
roles need to be created/edited at runtime or a user can hold multiple
roles. For this project, the three roles are fixed and each user has
exactly one, so an enum column is simpler and avoids an extra join on
every auth check. If multi-role-per-user is ever needed, this can be
migrated to a join table without changing the public API surface
(routes still receive a `current_user.role` string).

`values_callable` on the Enum column makes SQLAlchemy store the enum's
*value* ("student") in the database column, not its default behavior of
storing the member *name* ("STUDENT"). Either way the Python-side
attribute and the JSON API stay lowercase, but this keeps the raw SQLite
column matching what /docs and the JWT payload show, in case anyone
inspects the .db file directly.
"""

import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, String, Boolean
from sqlalchemy.orm import Mapped

from app.database.session import Base


class RoleEnum(str, enum.Enum):
    STUDENT = "student"
    RECRUITER = "recruiter"
    PLACEMENT_OFFICER = "placement_officer"


def _generate_uuid() -> str:
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = Column(String, primary_key=True, default=_generate_uuid)
    full_name: Mapped[str] = Column(String, nullable=False)
    email: Mapped[str] = Column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = Column(String, nullable=False)
    role: Mapped[str] = Column(
        Enum(RoleEnum, values_callable=lambda enum_cls: [e.value for e in enum_cls]),
        nullable=False,
        default=RoleEnum.STUDENT,
    )
    is_active: Mapped[bool] = Column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email} role={self.role}>"
