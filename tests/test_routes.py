def test_home_redirects_not_logged_in(client):
    response = client.get('/')
    assert response.status_code == 302

def test_add_contact_page_requires_login(client):
    response = client.get('/add')
    assert response.status_code == 302

def rest_contacts_page_requires_login(client):
    response = client.get('/contacts')
    assert response.status_code == 302 

def test_add_contact_succsess(client, auth):
    auth.login()
    response = client.post('/add', data={
        'name': 'Test Contact',
        'date': '2000-01-01'
    }, follow_redirects=True)

    assert b'Contact added successfully!' in response.data

def test_add_contact_missing_name(client, auth):
    auth.login()
    response = client.post('/add', data={
        'name': '',
        'date': '2000-01-01'
    }, follow_redirects=True)

    assert b'Error updating contact' in response.data

def test_edit_contact(client, auth, create_contact):
    auth.login()
    contact = create_contact(name='Original Name')
    response = client.post(f'/edit/{contact.id}', data={
        'name': 'Updated Name',
        'date': '2000-01-01'
    }, follow_redirects=True)

    assert b'Contact updated successfully!' in response.data

def test_delete_contact(client, auth, create_contact):
    auth.login()
    contact = create_contact(name='Delete Me')
    response = client.post(f'/delete/{contact.id}', follow_redirects=True)

    assert b'Contact Delete Me has been deleted' in response.data