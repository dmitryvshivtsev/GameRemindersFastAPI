from typing import Annotated
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import database.db_connect as db
import parsing as prs


templates = Jinja2Templates(directory="../templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="../static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/date", response_class=HTMLResponse)
def get_game_date(request: Request,
          kind_of_sport: Annotated[str, Form()],
          league:  Annotated[str, Form()],
          club: Annotated[str, Form()]):
    endpoint = {
        "is_finish": "False",
        "actual_score": None,
        "is_next_game": None,
        "club": club,
        "opponent": None,
        "next_game_date": None,
        "next_game_time": None
    }
    type_ = db.get_kinds_of_sport()
    league_ = db.get_league(kind_of_sport)
    club_ = db.get_team(league)
    if kind_of_sport in type_ and league in league_ and club in club_:
        team_tag = db.get_tag(club)
        return templates.TemplateResponse("game_date.html", {"request": request,
                                                             "match_info": prs.get_match(club=club,
                                                                                         team_tag=team_tag,
                                                                                         endpoint=endpoint)})
    else:
        return 'Error'


@app.get("/date", response_class=HTMLResponse)
def choose_team(request: Request):
    return templates.TemplateResponse("choose_team.html", {"request": request})
