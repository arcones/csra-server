from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# SQLite URL (using in-memory database for simplicity)
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Create async engine for SQLite
engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create sessionmaker for async use
SessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,  # AsyncSession for asynchronous DB operations
    expire_on_commit=False,
)
