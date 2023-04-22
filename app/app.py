import time

from fastapi import FastAPI, Form
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/")
def home():
    return FileResponse('../templates/home.html')


@app.post("/users")
def users(username = Form()):
    # если в базе данных нет такого логина, то будем регистрировать
    return {"login": username}

