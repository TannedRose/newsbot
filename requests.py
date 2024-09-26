from models import async_session,  User
from sqlalchemy import select, update, delete, BigInteger, text


async def add_user(user_id: BigInteger, name: str, username: str):
    async with async_session() as session:
        result = await session.execute(select(User.id).where(User.user_id == user_id))
        if result.scalar() is None:
            session.add(User(user_id=user_id, username=username))
        else:
            ...
        await session.commit()