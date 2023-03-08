from fastapi.testclient import TestClient
from app.database import get_db
from app.database import Base
from app.main import app
from app.config import settings
from app.oauth2 import create_access_token
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models
import pytest
from alembic import command

# SQLALCHEMY_DATABASE_URL = 'postgresql://emumba:emumba@localhost:8000/fastapi_test'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "hello1@gmail.com", "password": "password1"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "hello12@gmail.com", "password": "password12"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [{"title": "1st", "content": "1st", "user_id": test_user['id']},
                  {"title": "2nd", "content": "2nd", "user_id": test_user['id']},
                  {"title": "3rd", "content": "3rd", "user_id": test_user['id']},
                  {"title": "1st", "content": "1st", "user_id": test_user2['id']}]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    # session.add_all(models.Post(title="1st", content="1st", user_id=test_user['id']),
    #                 models.Post(title="2nd", content="2nd", user_id=test_user['id']),
    #                 models.Post(title="3rd", content="3rd", user_id=test_user['id']))
    session.commit()
    posts = session.query(models.Post).all()
    return posts
