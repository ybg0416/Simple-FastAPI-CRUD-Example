from uuid import UUID, uuid4

from pydantic import EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlmodel import AutoString, Field

from app.models import TableTimeStamp


class Member(TableTimeStamp, table=True):
    id: int = Field(primary_key=True, sa_column_kwargs={"comment": "사용자 PK"})
    uuid: UUID = Field(
        default_factory=uuid4,
        sa_column_kwargs={"comment": "사용자 UUID"},
        index=True,
    )

    email: EmailStr = Field(
        sa_type=AutoString,
        max_length=100,
        sa_column_kwargs={"comment": "사용자 이메일"},
        unique=True,
        nullable=False,
    )
    name: str = Field(max_length=32, sa_column_kwargs={"comment": "사용자 이름"})
    phone: PhoneNumber = Field(
        min_length=11,
        max_length=30,
        sa_column_kwargs={"comment": "사용자 전화번호"},
        nullable=False,
    )
