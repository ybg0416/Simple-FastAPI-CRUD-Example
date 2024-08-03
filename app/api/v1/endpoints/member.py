from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    status,
)
from loguru import logger
from pydantic import EmailStr
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.postgresql import get_db
from app.models import Member
from app.schemas import (
    CreateMember,
    InfoMember,
    UpdateMember,
)

router = APIRouter()


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "모든 멤버 반환",
        },
    },
)
async def get_all_member(db: AsyncSession = Depends(get_db)):
    """
    ### get All Members
    """
    return (await db.exec(select(Member))).all()


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "ID 해당하는 멤버 반환"},
        404: {
            "description": "존재하지 않는 멤버",
            "content": {"application/json": {"example": ""}},
        },
    },
)
async def get_member_by_id(
    member_id: int = Path(description="Member ID", alias="id"),
    db: AsyncSession = Depends(get_db),
) -> InfoMember:
    """
    ### get Member By ID
    """
    member = (await db.exec(select(Member).where(Member.id == member_id))).first()
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return InfoMember(**member.model_dump())


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "가입 Member 정보 반환"},
        400: {"description": "가입 실패(이메일 충돌)"},
        500: {"description": "가입 실패"},
    },
)
async def create_member(
    param: CreateMember, db: AsyncSession = Depends(get_db)
) -> InfoMember:
    """
    ### add Member
    """

    try:
        member = (
            await db.exec(select(Member).where(Member.email == param.email))
        ).first()

        if member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"email already exists : {member.email}",
            )

        new_member = Member(**param.model_dump())

        db.add(new_member)
        await db.commit()
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e
    logger.info(new_member)
    return InfoMember(**new_member.model_dump())


@router.put(
    "/{id}",
    responses={
        200: {"description": "수정 Member 정보 반환", "model": UpdateMember},
        409: {
            "description": "수정 실패",
            "content": {"application/json": {"example": ""}},
        },
        500: {
            "description": "수정 실패(이메일 충돌)",
            "content": {"application/json": {"example": ""}},
        },
    },
)
async def update_member(
    param: UpdateMember,
    member_id: int = Path(alias="id"),
    db: AsyncSession = Depends(get_db),
) -> InfoMember:
    """
    ### update Member
    """
    existing_memeber: Member = (
        await db.exec(select(Member).where(Member.id == member_id))
    ).first()

    # 기존 멤버 미존재
    if not existing_memeber:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Member not found"
        )
    # 이메일이 기존과 다르고, db에 변경한 이메일이 있는 경우
    if (
        existing_memeber.email != param.email
        and (await db.exec(select(Member).where(Member.email == param.email))).first()
    ):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Update Email already exists : {param.email}",
        )

    try:
        # data update
        existing_memeber.name = param.name
        existing_memeber.email = param.email
        existing_memeber.phone = param.phone

        await db.commit()
        await db.refresh(existing_memeber)

        return InfoMember(**existing_memeber.model_dump())
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT) from e


@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Member Email 사용 가능 여부 반환"},
    },
)
async def delete_member(
    member_id: int = Path(description="Member ID", alias="id"),
    db: AsyncSession = Depends(get_db),
):
    """
    ### delete Member
    """

    del_member = await db.get(Member, member_id)

    if not del_member:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Delete Member with id: {member_id} doesn't exist",
        )

    await db.delete(del_member)
    await db.commit()
    return None


@router.get(
    "/email/check/{email}",
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "사용 가능 여부"}},
)
async def check_email(
    email: EmailStr = Path(description="email"),
    db: AsyncSession = Depends(get_db),
) -> bool:
    """
    ### get Member By ID
    """
    return not (await db.exec(select(Member).where(Member.email == email))).first()
