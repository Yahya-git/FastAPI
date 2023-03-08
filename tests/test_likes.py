import pytest
from app import models


@pytest.fixture()
def test_like(test_posts, test_user, session):
    new_like = models.Likes(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_like)
    session.commit()


def test_like_on_post(authorized_client, test_posts):
    res = authorized_client.post(
        "/like/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 201


def test_already_liked(authorized_client, test_posts, test_like):
    res = authorized_client.post(
        "/like/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 409

def test_delete_like(authorized_client, test_posts, test_like):
    res = authorized_client.post(
        "/like/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201

def test_delete_like_not_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/like/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 404

def test_delete_like_on_post_not_exist(authorized_client, test_posts):
    res = authorized_client.post(
        "/like/", json={"post_id": 10, "dir": 1})
    assert res.status_code == 404

def test_unauthorized_like_post(client, test_posts):
    res = client.post(
        "/like/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 401