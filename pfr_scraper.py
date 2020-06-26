from bs4 import BeautifulSoup
import pandas as pd
import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class GameScraper:
    def __init__(self, url):
        self.url = url

    def create_df(self):
        res = requests.get(self.url)
        soup = BeautifulSoup(res.content, 'lxml')
        table = soup.find_all('table')[0]
        df = pd.read_html(str(table))
        df = df[0]
        df_col0 = df.columns.get_level_values(0)
        df_col1 = df.columns.get_level_values(1)
        col_list = []
        for idx, each in enumerate(df_col0):
            if each.startswith('Unnamed'):
                zero_lvl = ""
            else:
                zero_lvl = each + ' | '
            if df_col1[idx].startswith('Unnamed'):
                one_lvl = 'Index_' + str(idx)
            else:
                one_lvl = df_col1[idx]
            col_list.append(zero_lvl + one_lvl)
        df.columns = col_list
        df = df[pd.to_numeric(df['Rk'], errors='coerce').notnull()]
        return df


class DatabaseMaker:
    def __init__(self, db):
        self.db = db

    def create_db(self):
        Base = declarative_base()

        class GameLog(Base):
            __tablename__ = 'gamelog'

            id = Column('id', Integer, primary_key=True)
            player_id = Column('player_id', String)