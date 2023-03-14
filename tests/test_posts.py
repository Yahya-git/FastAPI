import pytest

from app import schemas

# trunk-ignore(flake8/F401)
from tests.conftest import authorized_client


# trunk-ignore(flake8/F811)
def test_get_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    # posts = schemas.PostOut(res.json())
    def validate(post):
        return schemas.PostOut(**post)

    # posts_map = map(validate, res.json())
    # posts_list = list(posts_map)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


# trunk-ignore(flake8/F811)
def test_get_single_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f'{"posts/10"}')
    assert res.status_code == 404


# trunk-ignore(flake8/F811)
def test_get_single_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


@pytest.mark.parametrize(
    "title, content, publish",
    [
        ("new title", "new content", True),
        ("new title 1", "new content 1", True),
        ("new title 2", "new content 2", True),
    ],
)
def test_create_posts(
    # trunk-ignore(flake8/F811)
    authorized_client,
    test_user,
    test_posts,
    title,
    content,
    publish,
):
    res = authorized_client.post(
        f'{"/posts/"}', json={"title": title, "content": content, "publish": publish}
    )

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.publish == publish
    assert created_post.user_id == test_user["id"]


def test_unauthorized_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


# trunk-ignore(flake8/F811)
def test_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


# trunk-ignore(flake8/F811)
def test_delete_post_not_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f'{"/posts/10"}')
    assert res.status_code == 404


# trunk-ignore(flake8/F811)
def test_delete_others_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


# trunk-ignore(flake8/F811)
def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


# trunk-ignore(flake8/F811)
def test_update_others_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id,
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_update_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


# trunk-ignore(flake8/F811)
def test_update_post_not_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id,
    }
    res = authorized_client.put(f'{"/posts/10"}', json=data)
    assert res.status_code == 404
