import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src import models, crud, schemas
from src.database import get_db
from src.main import app
from src.security import create_access_token


DB_URL_TEST = 'sqlite:///./sqlite_test.db'

engine_test = create_engine(
    DB_URL_TEST,
    connect_args={'check_same_thread': False}
)

TestingSessionLocal = sessionmaker(bind=engine_test, autoflush=False, autocommit=False)

def override_get_db():
    db = TestingSessionLocal()
    try: 
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope='session')
def prepare_database():
    models.Base.metadata.drop_all(engine_test)
    models.Base.metadata.create_all(bind=engine_test)


@pytest.fixture(scope='session')
def mock_users():
    db = TestingSessionLocal()
    for i in range(1, 6):
        crud.create_user(db=db, request=get_fake_user(i))       
    db.close()


@pytest.fixture(scope='module')
def mock_posts():
    db = TestingSessionLocal()
    for i in range(1, 3):
        crud.create_post(db=db, request=get_fake_post(i))       
    db.close()


def get_fake_user(num: int) -> schemas.UserWrite:
    fake_user = schemas.UserWrite(
        name=f'FakeUser{num}',
        email=f'FakeUser{num}@test.com',
        password=f'password'
    )
    return fake_user


def get_fake_post(user_id: int) -> schemas.PostWrite:
    fake_post = schemas.PostWrite(
        title=f'Fake Post {user_id}',
        content=f'Fake Post {user_id} content',
        user_id=user_id
    )
    return fake_post

@pytest.fixture(scope='module')
def creator_access_token():
    fake_user = get_fake_user(1)
    creator_access_token = create_access_token(
        data={'sub': fake_user.name}
    )
    return creator_access_token


@pytest.fixture(scope='module')
def reviewer_access_token():
    fake_user = get_fake_user(5)
    reviewer_access_token = create_access_token(
        data={'sub': fake_user.name}
    )
    return reviewer_access_token
