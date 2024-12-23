import requests
import json

# Clear all services
requests.get("http://127.0.0.1:9000/clear")
requests.get("http://127.0.0.1:9001/clear")
requests.get("http://127.0.0.1:9002/clear")
requests.get("http://127.0.0.1:9003/clear")

# Create a user
create_user_url = "http://127.0.0.1:9000/create_user"
user_data = {
    'first_name': 'John',
    'last_name': 'Doe',
    'username': 'johndoe',
    'email_address': 'john@example.com',
    'password': 'Password123',
    'group': 'users',
    'salt': 'random_salt'
}
response = requests.post(create_user_url, data=user_data)
print("Create User Response:", response.json())

# Attempt to create another user with the same username
user_data['email_address'] = 'john2@example.com'  # Change email to avoid email conflict
response = requests.post(create_user_url, data=user_data)
print("Attempt to Create Duplicate Username Response:", response.json())

# Attempt to create another user with the same email
user_data['username'] = 'johnnydoe'  # Change username to avoid username conflict
user_data['email_address'] = 'john@example.com'  # Reuse existing email
response = requests.post(create_user_url, data=user_data)
print("Attempt to Create Duplicate Email Response:", response.json())


login_url = "http://127.0.0.1:9000/login"
login_data = {
    'username': 'johndoe',
    'password': 'WrongPassword'
}
response = requests.post(login_url, data=login_data)
print("Login with Wrong Password Response:", response.json())



create_document_url = "http://127.0.0.1:9001/create_document"
document_data = {
    'filename': 'test.txt',
    'body': 'This is a test document.',
    'groups': json.dumps({'group1': 'users'})
}
# Do not include Authorization header
response = requests.post(create_document_url, data=document_data)
print("Create Document Without JWT Response:", response.json())


# Login as johndoe
response = requests.post(login_url, data={'username': 'johndoe', 'password': 'Password123'})
jwt_johndoe = response.json()['jwt']

# Create a document as johndoe
headers = {'Authorization': jwt_johndoe}
response = requests.post(create_document_url, data=document_data, headers=headers)
print("Create Document Response:", response.json())

# Create another user in a different group
user_data = {
    'first_name': 'Jane',
    'last_name': 'Smith',
    'username': 'janesmith',
    'email_address': 'jane@example.com',
    'password': 'Password123',
    'group': 'admins',
    'salt': 'random_salt2'
}
response = requests.post(create_user_url, data=user_data)
print("Create Another User Response:", response.json())

# Login as janesmith
response = requests.post(login_url, data={'username': 'janesmith', 'password': 'Password123'})
jwt_janesmith = response.json()['jwt']

# Attempt to edit the document as janesmith
edit_document_url = "http://127.0.0.1:9001/edit_document"
edit_data = {
    'filename': 'test.txt',
    'body': 'Adding unauthorized content.'
}
headers = {'Authorization': jwt_janesmith}
response = requests.post(edit_document_url, data=edit_data, headers=headers)
print("Edit Document Without Permission Response:", response.json())


search_document_url = "http://127.0.0.1:9002/search"
search_params = {'filename': 'test.txt'}
headers = {'Authorization': jwt_janesmith}
response = requests.get(search_document_url, params=search_params, headers=headers)
print("Search Document Without Permission Response:", response.json())


view_log_url = "http://127.0.0.1:9003/view_log"
log_params = {'username': 'johndoe'}
headers = {'Authorization': jwt_janesmith}
response = requests.get(view_log_url, params=log_params, headers=headers)
print("View Logs for Another User Response:", response.json())


invalid_jwt = 'invalid.jwt.token'
headers = {'Authorization': invalid_jwt}
response = requests.post(create_document_url, data=document_data, headers=headers)
print("Create Document with Invalid JWT Response:", response.json())
