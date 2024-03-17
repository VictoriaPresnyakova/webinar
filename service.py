from typing import AsyncIterator

from sqlalchemy import select

from database import get_session, User as UserDB, StatusEnum
from dto import User


async def save_user(user: User) -> User:
    async with get_session() as session:
        user_db_instance = UserDB(
            id=user.id, created_at=user.created_at, status=user.status,
            status_updated_at=user.status_updated_at,
            msg_num=user.msg_num, msg_to_send_at=user.msg_to_send_at
        )
        session.add(user_db_instance)
        await session.commit()
        await session.refresh(user_db_instance)
        return user_db_instance


async def update_user(new_user: User) -> User:
    async with (get_session() as session):
        # Fetch the tutorial from the database
        user_db_instance = await session.get(UserDB, new_user.id)

        if user_db_instance is None:
            raise ValueError("User not found")

        # Update
        user_db_instance.status = new_user.status
        user_db_instance.status_updated_at = new_user.status_updated_at
        user_db_instance.msg_num = new_user.msg_num
        user_db_instance.msg_to_send_at = new_user.msg_to_send_at

        # Commit changes to the database
        await session.commit()
        await session.refresh(user_db_instance)

        # Return the updated user
        return UserDB(id=user_db_instance.id, created_at=user_db_instance.created_at, status=user_db_instance.status,
                    status_updated_at=user_db_instance.status_updated_at,
                    msg_num=user_db_instance.msg_num, msg_to_send_at=user_db_instance.msg_to_send_at)


async def list_users() -> AsyncIterator[User]:
    async with get_session() as session:
        query = await session.execute(select(UserDB))
        users_db = query.scalars().all()

        for user_db in users_db:
            yield User(id=user_db.id, created_at=user_db.created_at, status=user_db.status,
                       status_updated_at=user_db.status_updated_at,
                       msg_num=user_db.msg_num, msg_to_send_at=user_db.msg_to_send_at)


async def list_alive_users() -> AsyncIterator[User]:
    async with get_session() as session:
        query = await session.execute(select(UserDB).where(UserDB.status == StatusEnum.ALIVE))
        users_db = query.scalars().all()

        for user_db in users_db:
            yield User(id=user_db.id, created_at=user_db.created_at, status=user_db.status,
                       status_updated_at=user_db.status_updated_at,
                       msg_num=user_db.msg_num, msg_to_send_at=user_db.msg_to_send_at)
