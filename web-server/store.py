import requests as req

def get_users():
    R = req.get('https://api.escuelajs.co/api/v1/users')
    print(type(R.text))
    print(R)
    print(R.status_code)
    print(R.text)

    Users = R.json()
    print(type(Users))
    print(Users)

    for User in Users:
        print(User['name'])