from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedColumn, Relationship, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs


engine = create_async_engine(url='sqlite+aiosqlite:///db1.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(default="None")
    username: Mapped[str] = mapped_column(nullable=False)
    banned: Mapped[int] = mapped_column(default=0)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
