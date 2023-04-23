from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
import database.db_connect as db
import parsing as prs


app = FastAPI()


@app.get("/")
def home():
    return FileResponse('../templates/home.html')


@app.post("/date")
def users(kind_of_sport=Form(), league=Form(), club=Form()):
    type_ = db.get_kinds_of_sport()
    league_ = db.get_league(str(kind_of_sport))
    club_ = db.get_team(str(league))
    if kind_of_sport in type_ and league in league_ and club in club_:
        team_tag_ = db.get_tag(str(club))
        return prs.get_match(club, team_tag_)
    else:
        return "Ошибка"
