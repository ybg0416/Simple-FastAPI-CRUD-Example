from uuid import UUID

from pydantic import AwareDatetime, BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber


class MemberBase(BaseModel):
    name: str = Field(title="ID of the user", examples=["홍길동"])
    email: EmailStr = Field(title="Email of the user", examples=["test@naver.com"])
    phone: PhoneNumber = Field(title="phone number", examples=["+821012345678"])


class CreateMember(MemberBase):
    pass


class UpdateMember(MemberBase):
    pass


class InfoMember(MemberBase):
    uuid: UUID = Field(
        title="UUID of the user", examples=["123e4567-e89b-12d3-a456-426614174001"]
    )
    id: int = Field(title="ID of the user", examples=["1"])

    # TODO(ybg) 240728 pydantic 2.8x datetime 관련
    #  https://github.com/pydantic/pydantic/issues/9571, https://github.com/pydantic/pydantic/issues/8683
    reg_dt: AwareDatetime = Field(
        title="Created at",
        description="The date and time that the user was created",
        examples=["2023-05-04T01:05:54.988Z"],
    )
    mod_dt: AwareDatetime = Field(
        title="Updated at",
        description="The date and time that the user was updated",
        examples=["2023-05-04T01:05:54.988Z"],
    )
