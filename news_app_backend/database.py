import pandas
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine(
    "sqlite+aiosqlite:///users.db"
)
session = async_sessionmaker(engine, expire_on_commit=False)
print(pandas.DataFrame())


class UsersTable(DeclarativeBase):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    region: Mapped[str]


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(UsersTable.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(UsersTable.metadata.drop_all)
