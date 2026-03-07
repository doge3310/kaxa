# import socket
from datetime import datetime
from fastapi import FastAPI, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from uvicorn import run
from playhouse.shortcuts import model_to_dict
from pydantic import BaseModel

from db import User, Message
from hasher import hash_password, verify_password


app = FastAPI()
auf_token = OAuth2PasswordBearer(tokenUrl="token")


class MessagePost(BaseModel):
    from_name: str
    to_name: str
    text: str


class NewUser(BaseModel):
    name: str
    password: str


async def get_current_user(name: str = Depends(auf_token)):
    user = User.get_or_none(name=name)

    if not user:
        raise HTTPException(status_code=400, detail="invalid name")

    return user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = User.get_or_none(name=form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="invalid name")

    user = model_to_dict(user)

    if verify_password(form_data.password, user["password"]):
        return {"access_token": user["name"]}

    raise HTTPException(status_code=400, detail="invalid password")


@app.post("/register")
def register(data: NewUser = Body()):
    user = User.get_or_none(
        name=data.name
    )

    if user:
        raise HTTPException(status_code=409, detail="user already exist")

    user = User.create(
        name=data.name,
        password=hash_password(data.password)
    )

    return user


@app.delete("/deleteUser")
def delete_user(data: NewUser = Body(), current_user: User = Depends(auf_token)):
    user: User = User.get_or_none(
        name=data.name
    )

    if not user:
        raise HTTPException(status_code=400, detail="invalid name or already deleted")

    if verify_password(data.password, user.password):
        messages = Message.select().where(Message.from_user == user.id or
                                          Message.to_user == user.id)

        for i in messages:
            i.delete_instance()

        user.delete_instance()

        return True

    raise HTTPException(status_code=400, detail="Invalid password")


# @app.get("/ip")
# async def get_ip():
#     host = socket.gethostname()
#     host_ip = socket.gethostbyname(host)

#     return host_ip


@app.get("/messages")
async def user_message(current_user: User = Depends(get_current_user)):
    user = User.get_or_none(name=current_user.name)

    if not user:
        raise HTTPException(status_code=400, detail="invalid name")

    messages = Message.select().where((Message.from_user == user) |
                                      (Message.to_user == user))

    return [(model_to_dict(i)["text"],
             model_to_dict(i)["from_user"]["name"],
             model_to_dict(i)["to_user"]["name"],
             model_to_dict(i)["time"])
            for i in messages]


@app.post("/postMessage")
async def post_message(data: MessagePost = Body(), current_user: User = Depends(get_current_user)):
    if data.from_name != current_user.name:
        raise HTTPException(status_code=403, detail="Cannot send not your messages")

    from_user = User.get_or_none(name=data.from_name)
    to_user = User.get_or_none(name=data.to_name)
    time = datetime.now()

    message, _ = Message.get_or_create(
        text=data.text,
        time=time,
        from_user=from_user,
        to_user=to_user
    )

    message = model_to_dict(message)

    return (message["text"],
            message["time"],
            message["from_user"]["name"],
            message["to_user"]["name"])


@app.get("/users")
async def get_users(current_user: User = Depends(auf_token)):
    return [model_to_dict(i)["name"] for i in User.select()]


if __name__ == "__main__":
    run("api:app", host="0.0.0.0", port=8000, reload=True)
