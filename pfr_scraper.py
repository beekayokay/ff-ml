from datetime import datetime

from bs4 import BeautifulSoup
import pandas as pd
import requests
from sqlalchemy import create_engine
from sqlalchemy.types import Float, Integer, String


class GameScraper:
    def __init__(self, url):
        self.url = url

    def create_df(self, col, count):
        page = requests.get(self.url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, "lxml")
            table = soup.find('tbody')
            rows = table.findAll('tr')
        df = pd.DataFrame(columns=col)
        for idx, item in enumerate(rows):
            data_set = rows[idx].findAll('td')
            if len(data_set) > 0:
                for idx, item in enumerate(data_set):
                    if idx == 0:
                        df.loc[count, 'player_id'] = item['data-append-csv']
                        df.loc[count, 'player'] = item.text
                    else:
                        if item['data-stat'] in col:
                            try:
                                df.loc[count, item['data-stat']] = (
                                    (datetime.strptime(item.text, '%Y-%m-%d') -
                                        datetime(1970, 1, 1)).total_seconds()
                                )
                            except ValueError:
                                try:
                                    df.loc[count, item['data-stat']] = (
                                        round(float(item.text), 4)
                                    )
                                except ValueError:
                                    df.loc[count, item['data-stat']] = item.text
                count += 1
        df.log_id = (
            df.player_id + '-' +
            df.game_date.astype(int).astype(str) + '-' +
            df.week_num.astype(int).astype(str)
        )
        df['fantasy_points'] = df['fantasy_points'].replace('', 0)
        df['fantasy_points_ppr'] = df['fantasy_points_ppr'].replace('', 0)
        df['draftkings_points'] = df['draftkings_points'].replace('', 0)
        df['fanduel_points'] = df['fanduel_points'].replace('', 0)
        return df


class DatabaseMaker:
    def __init__(self, df):
        self.df = df

    def create_db(self):
        engine = create_engine('sqlite:///test.db', echo=True)
        table_name = 'gamelogs'
        self.df.to_sql(
            table_name,
            con=engine,
            if_exists='append',
            index=True,
            # chunksize=500,
            dtype={
                'log_id': String,
                'player_id': String,
                'player': String,
                'pos': String,
                'age': Float,
                'game_date': Integer,
                'league_id': String,
                'team': String,
                'game_location': String,
                'opp': String,
                'game_result': String,
                'game_num': Integer,
                'week_num': Integer,
                'game_day_of_week': String,
                'fantasy_points': Float,
                'fantasy_points_ppr': Float,
                'draftkings_points': Float,
                'fanduel_points': Float,
                'pass_cmp': Integer,
                'pass_att': Integer,
                'pass_yds': Integer,
                'pass_td': Integer,
                'pass_int': Integer,
                'rush_att': Integer,
                'rush_yds': Integer,
                'rush_td': Integer,
                'rec': Integer,
                'rec_yds': Integer,
                'rec_td': Integer,
                'fumbles': Integer,
                'fgm': Integer,
                'fga': Integer,
                'xpm': Integer,
                'xpa': Integer
            }
        )
