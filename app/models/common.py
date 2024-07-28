from pydantic import AwareDatetime
from sqlmodel import DateTime, Field, SQLModel, func


class TableTimeStamp(SQLModel):
    # TODO(ybg) 240728 아직도 안고쳐짐..
    #  여러 테이블에서 Column 또는 sa_column 사용 시
    #  Column object 'Column' already assigned to Table 'Table' -> https://github.com/tiangolo/sqlmodel/discussions/743
    # reg_dt = Column(
    #     "reg_dt",
    #     sa_type=TIMESTAMP(timezone=True),
    #     server_default=func.now(),
    #     nullable=False,
    # )

    # mod_dt = Column(
    #     "mod_dt",
    #     sa_type=TIMESTAMP(timezone=True),
    #     server_default=func.now(),
    #     server_onupdate=func.now(),
    #     nullable=False,
    # )

    reg_dt: AwareDatetime = Field(
        sa_type=DateTime(True),
        nullable=False,
        sa_column_kwargs={"server_default": func.now(), "comment": "등록일"},
    )
    mod_dt: AwareDatetime = Field(
        sa_type=DateTime(True),
        nullable=False,
        sa_column_kwargs={
            "server_default": func.now(),
            "server_onupdate": func.now(),
            "comment": "수정일",
        },
    )
