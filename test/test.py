from requests import get, post

print(get('http://localhost:5000/api/users').json())
print(get('http://localhost:5000/api/users/1').json())
print(post('http://localhost:5000/api/users', json={
    'id': 1, 'name': 'Mike', 'surname': 'Smith', 'city': 'module_2',
    'email': 'smith@mars.org', 'age': 23, 'hashed_password': 'physics'}).json())
print(get('http://localhost:5000/api/users/8').json())