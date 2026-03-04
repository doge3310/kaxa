import requests


def send_message(server_ip: str, token: str, from_user: str, to_user: str, message: str) -> None:
    req = requests.post(
        url=f"http://{server_ip}:8000/postMessage",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "from_name": from_user,
            "to_name": to_user,
            "text": message
        },
        timeout=1000
    )


def register(server_ip: str, name: str, password: str) -> None:
    req = requests.post(
        url=f"http://{server_ip}:8000/register",
        json={
            "name": name,
            "password": password
        },
        timeout=1000
    )


def login(server_ip: str, name: str, password: str) -> str:
    req = requests.post(
        url=f"http://{server_ip}:8000/token",
        data={
            "username": name,
            "password": password
        },
        timeout=1000
    )

    return req.json()["access_token"]


def delete_user(server_ip: str, token: str, name: str, password: str) -> None:
    req = requests.delete(
        url=f"http://{server_ip}:8000/deleteUser",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": name,
            "password": password
        },
        timeout=1000
    )


def get_messages(server_ip: str, token: str) -> list:
    req = requests.get(
        url=f"http://{server_ip}:8000/messages",
        headers={"Authorization": f"Bearer {token}"},
        timeout=1000
    )

    return req.json()


def get_users(server_ip: str, token: str) -> list:
    req = requests.get(
        url=f"http://{server_ip}:8000/users",
        headers={"Authorization": f"Bearer {token}"},
        timeout=1000
    )

    return req.json()


print(get_messages("192.168.1.7", "user1"))
