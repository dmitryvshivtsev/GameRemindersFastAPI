from typing import Annotated
from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import database.db_connect as db
import parsing as prs


templates = Jinja2Templates(directory="../templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="../static"), name="static")

@app.get("/")
def root():
    return {"home": "page"}


@app.post("/date", response_class=HTMLResponse)
def users(request: Request, kind_of_sport: Annotated[str, Form()], league:  Annotated[str, Form()], club: Annotated[str, Form()]):
    type_ = db.get_kinds_of_sport()
    league_ = db.get_league(kind_of_sport)
    club_ = db.get_team(league)
    if kind_of_sport in type_ and league in league_ and club in club_:
        team_tag_ = db.get_tag(club)
        return templates.TemplateResponse("date.html", {"request": request, "match_info": prs.get_match(club, team_tag_)})
    else:
        return "Ошибка"


@app.get("/date")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
