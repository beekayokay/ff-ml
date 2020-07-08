import time

from configparser import ConfigParser

from pfr_scraper import GameScraper, DatabaseMaker

page_off = 0

year1 = 2002
year2 = 2019
col_list = [
    'log_id', 'team', 'year_id', 'game_date', 'gametime', 'local_time',
    'game_location', 'opp', 'week_num', 'game_num', 'game_day_of_week',
    'game_result', 'overtime', 'tot_yds', 'plays_offense',
    'yds_per_play_offense', 'plays_defense', 'yds_per_play_defense',
    'turnovers', 'time_of_poss', 'duration'
]

while int(page_off) < 9200:
    config_parser = ConfigParser()
    config_parser.read('config.ini')
    page_off = config_parser.get('SETTINGS', 'team_off')
    counter = config_parser.get('SETTINGS', 'team_db_count')

    url = (
        'https://www.pro-football-reference.com/play-index/tgl_finder.cgi'
        f'?request=1&match=game&year_min={year1}&year_max={year2}'
        '&game_type=R&game_num_min=0&game_num_max=99&week_num_min=0'
        '&week_num_max=99&temperature_gtlt=lt&c5val=1.0&order_by=plays_offense'
        f'&offset={page_off}'
    )

    game_scrape = GameScraper(url)
    df = game_scrape.create_team_df(col_list, int(counter))
    db_maker = DatabaseMaker(df)
    db_maker.create_team_db()

    config_parser.set('SETTINGS', 'team_off', str(int(page_off) + 100))
    config_parser.set('SETTINGS', 'team_db_count', str(int(counter) + 100))
    with open('config.ini', 'w') as configfile:
        config_parser.write(configfile)

    print(f'PAGE OFFSET: {page_off}')
    print(f'DB COUNTER: {counter}')

    time.sleep(10)
