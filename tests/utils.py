from app.models import User


def register(username, email="username@test.com", password="password"):
    user = User(username=username, email=email, password=password)
    user.save()
    print(user.id)
    return user.id


def login(client, username, email="username@test.com", password="password"):
    return client.post(
        "/api/login", json=dict(username=username, email=email, password=password), follow_redirects=True
    )


def logout(client):
    return client.get("/api/logout", follow_redirects=True)
