from conftest import client


def test_create_reaction(
    prepare_database,
    mock_users,
    mock_posts,
    reviewer_access_token
):
    response = client.post(
        '/reactions/1',
        headers={'Authorization': f'Bearer {reviewer_access_token}'},
        json={'is_like': True}
    )

    assert response.status_code == 201


def test_update_reaction(
    prepare_database,
    mock_users,
    mock_posts,
    reviewer_access_token
):
    response = client.put(
        '/reactions/1',
        headers={'Authorization': f'Bearer {reviewer_access_token}'},
        json={'is_like': False}
    )

    assert response.status_code == 202


def test_remove_reaction(
    prepare_database,
    mock_users,
    mock_posts,
    reviewer_access_token
):
    response = client.delete(
        '/reactions/1',
        headers={'Authorization': f'Bearer {reviewer_access_token}'},
    )

    assert response.status_code == 204
