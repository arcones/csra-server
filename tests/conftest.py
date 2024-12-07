import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from csra_server.database import Base, get_db
from csra_server.main import app

# Define the test database URL (SQLite in-memory database for testing)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create the test engine and session
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)
TestSessionLocal = sessionmaker(bind=test_engine, class_=AsyncSession, expire_on_commit=False)

# Fixture to set up the test database
@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    """Initialize the test database and create tables."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield  # After tests are done, clean-up happens automatically

# Fixture to provide a database session for tests
@pytest.fixture()
async def test_db():
    """Provide a transactional scope for test cases."""
    async with TestSessionLocal() as session:
        yield session  # Provide session to the test
        await session.rollback()  # Rollback changes after each test

# Fixture to provide a test client with the test database
@pytest.fixture()
async def client(test_db):
    """Override the `get_db` dependency and provide an async test client."""
    def override_get_db():
        """Override FastAPI's dependency to use the test database session."""
        return test_db

    app.dependency_overrides[get_db] = override_get_db  # Apply override

    async with AsyncClient(app=app, base_url="http://testserver") as test_client:
        yield test_client  # Provide the test client to the test
