import os

import sqlalchemy as db
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session
from sqlalchemy import select

engine = create_engine(os.getenv('DB_CONNECT'))
connection = engine.connect()


def get_kinds_of_sport():
    query = connection.execute(db.text("SELECT DISTINCT kind_of_sport FROM teams")).fetchall()
    result = []
    [result.append(*res) for res in query]
    return result


def get_league(kind: str):
    query = connection.execute(db.text(f"SELECT DISTINCT league FROM teams WHERE kind_of_sport = '{kind}'")).fetchall()
    result = []
    [result.append(*res) for res in query]
    return result


def get_team(league: str):
    query = connection.execute(db.text(f"SELECT DISTINCT team FROM teams WHERE league = '{league}'")).fetchall()
    result = []
    [result.append(*res) for res in query]
    return result


def get_tag(team: str):
    query = connection.execute(db.text(f"SELECT team_tag FROM teams WHERE team = '{team}'")).fetchall()
    return query[0][0]