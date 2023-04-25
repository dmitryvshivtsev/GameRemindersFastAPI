from bs4 import BeautifulSoup
import requests
import lxml
from datetime import datetime, date


def get_match(club: str, team_tag: str) -> dict:
    url = f'https://www.sports.ru/{team_tag}/calendar'
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    endpoint = {
        "is_finish": "False",
        "actual_score": None,
        "club": club,
        "opponent": None,
        "next_game_date": None,
        "next_game_time": None
    }

    now = datetime.now()
    dates = parse_date(soup)

    opps = parse_opp(soup)
    is_finish = finish_game(soup)
    last_result = last_game_result(soup=soup, is_finish=is_finish)

    for i, date_time in enumerate(dates):
        # Формат на сайте лежит в виде "Дата | Время" или "Дата"
        date_time = date_time.split('|')
        if len(date_time) > 1 or not date_time[0].isalpha():
            elems = date_time[0].split('.')
            if not elems[0].isalpha():
                cur_day, cur_month, cur_year = map(int, elems)
                parsed_date = date(cur_year, cur_month, cur_day)
                now_time = datetime.now().strftime("%H:%M")
                if (parsed_date.month == now.month and parsed_date.day >= now.day) or \
                        (parsed_date.month > now.month and parsed_date.year >= now.year):
                    if date_time[1] <= now_time and parsed_date.day == now.day:
                        if not is_finish:
                            endpoint.update([('is_finish', "False"), ('actual_score', last_result)])
                            return endpoint
                        if is_finish:
                            endpoint.update([('is_finish', 'True'), ('actual_score', last_result)])
                            return endpoint
                    elif len(date_time) > 1:
                        endpoint.update([('is_finish', 'True'), ('actual_score', last_result), ('opponent', opps[i]),
                                         ('next_game_date', parsed_date.strftime('%d.%m.%Y')),
                                         ('next_game_time', date_time[1])])
                        return endpoint
                    else:
                        endpoint.update([('is_finish', 'True'), ('actual_score', last_result), ('opponent', opps[i]),
                                         ('next_game_date', parsed_date.strftime('%d.%m.%Y'))])
                        return endpoint


def parse_date(soup: BeautifulSoup) -> list:
    dates = []
    for date_ in soup.find_all('td', class_='name-td alLeft bordR'):
        if not date_.text.isalpha():
            dates.append(date_.text.strip())

    return dates


def parse_opp(soup: BeautifulSoup) -> list:
    opps = []
    for opp in soup.find_all('div', class_='hide-field'):
        opps.append(opp.text.strip())
    new_opps = []
    for i in range(len(opps)):
        if i % 2 == 1:
            new_opps.append(opps[i])
    return new_opps


# is it necessary?
def parse_score(soup: BeautifulSoup) -> list:
    scores = []
    for score in soup.find_all('td', class_='score-td'):
        scores.append(score.text.strip())
    return scores


def finish_game(soup: BeautifulSoup) -> bool:
    is_finish = False
    for st in soup.find('div', class_='score-descr'):
        if st.text.strip() == 'завершен':
            is_finish = True
    return is_finish


# this must be rewritten
def check_place(soup: BeautifulSoup, scores: list) -> list:
    where_game = []
    for place in soup.find_all('td', class_='alRight padR20'):
        if place.text.strip():
            where_game.append(place.text.strip())
    for i, place in enumerate(where_game):
        if place == 'В гостях':
            pass
    return scores


def last_game_result(soup: BeautifulSoup, is_finish: bool) -> str:
    commands = []
    score = []
    for teams in soup.find('div', class_='commands').find_all('a'):
        commands.append(teams.text.strip())
    if is_finish:
        try:
            board = soup.find('div', class_='score score-green').find_all('span')
        except AttributeError:
            try:
                board = soup.find('div', class_='score score-red').find_all('span')
            except AttributeError:
                board = soup.find('div', class_='score score-orange').find_all('span')
    else:
        board = soup.find('div', class_='score score-gray').find_all('span')
    for num in board:
        score.append(num.text.strip())
    return f"{commands[0]} [ {score[0]} : {score[1]} ] {commands[1]}"

