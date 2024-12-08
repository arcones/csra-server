from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./csra.db"

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True, future=True)

SessionLocal = sessionmaker(
    bind=engine,  # Use 'bind' to associate the engine
    class_=AsyncSession,  # AsyncSession for asynchronous DB operations
    expire_on_commit=False
)

# Declarative base for defining models
Base = declarative_base()

# Function to initialize the database
async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
