from typing import Annotated

from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from pydantic.main import BaseModel

import database.db_connect as db
import parsing as prs


templates = Jinja2Templates(directory="../templates")

app = FastAPI()

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/date")
def users(kind_of_sport: Annotated[str, Form()], league:  Annotated[str, Form()], club: Annotated[str, Form()]):
    type_ = db.get_kinds_of_sport()
    league_ = db.get_league(kind_of_sport)
    club_ = db.get_team(league)
    if kind_of_sport in type_ and league in league_ and club in club_:
        team_tag_ = db.get_tag(club)
        return prs.get_match(club, team_tag_)
    else:
        return "Ошибка"


@app.get("/date")
def root():
    return FileResponse("../templates/home.html")
