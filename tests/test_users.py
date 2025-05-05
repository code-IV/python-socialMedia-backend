import pytest

from conftest import client


admin = {
    'name': 'admin',
    'email': 'admin@admin.com',
    'password': 'admin'
}


@pytest.mark.first
def test_create_user(prepare_database):
    response = client.post('/users', json=admin)
    assert response.status_code == 201


def test_get_user(prepare_database):
    response = client.get('/users/6')
    assert response.status_code == 200
    assert response.json()['name'] == admin['name']
    assert response.json()['email'] == admin['email']