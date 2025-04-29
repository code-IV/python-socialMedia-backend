from conftest import client


fake_post ={
    'title': 'Fake post 1',
    'content': 'Fake post 1 content',
    'user_id': 1
}

def test_create_post(
    prepare_database, 
    mock_users,
    creator_access_token
):
    response = client.post(
        '/posts/',
        headers={'Authorization': f'Bearer {creator_access_token}'},
        json=fake_post
    )

    assert response.status_code == 201


def test_update_post(
    prepare_database, 
    mock_users,
    creator_access_token
):
    response = client.put(
        '/posts/1',
        headers={'Authorization': f'Bearer {creator_access_token}'},
        json=fake_post
    )

    assert response.status_code == 202
    

def test_delete_post(
    prepare_database, 
    mock_users,
    creator_access_token
):
    response = client.delete(
        '/posts/1',
        headers={'Authorization': f'Bearer {creator_access_token}'}
    )

    assert response.status_code == 204
