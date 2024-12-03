import asyncio

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)

from database.tables.base import Base

engine = create_async_engine(
    "sqlite+aiosqlite:///database/data/bot.db",
    connect_args={"check_same_thread": False},
    echo=False,
)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


# async def insert_default_group():
#     async with async_session() as session:
#         async with session.begin():
#             result = await session.execute(select(Group).where(Group.name == "默认"))
#             if not result.scalars().first():
#                 session.add(
#                     Group(
#                         id=0,
#                         name="默认",
#                         from_currency=cfg.from_currency,
#                         to_currency=cfg.to_currency,
#                         default=True,
#                     )
#                 )


def init_db() -> None:
    async def fn():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            # await insert_default_group()

    asyncio.get_event_loop().create_task(fn())


init_db()
