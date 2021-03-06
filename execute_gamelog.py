import time

from configparser import ConfigParser

from pfr_scraper import GameScraper, DatabaseMaker

page_off = 0

year1 = 2002
year2 = 2019
col_list = [
    'log_id', 'player_id', 'player', 'pos', 'age', 'game_date', 'league_id',
    'team', 'game_location', 'opp', 'game_result', 'game_num', 'week_num',
    'game_day_of_week', 'fantasy_points', 'fantasy_points_ppr',
    'draftkings_points', 'fanduel_points', 'pass_cmp', 'pass_att', 'pass_yds',
    'pass_td', 'pass_int', 'rush_att', 'rush_yds', 'rush_td', 'rec', 'rec_yds',
    'rec_td', 'fumbles', 'fgm', 'fga', 'xpm', 'xpa'
]

while int(page_off) < 120000:
    config_parser = ConfigParser()
    config_parser.read('config.ini')
    page_off = config_parser.get('SETTINGS', 'offset')
    counter = config_parser.get('SETTINGS', 'db_counter')

    url = (
        'https://www.pro-football-reference.com/play-index/pgl_finder.cgi?'
        f'request=1&match=game&year_min={year1}&year_max={year2}'
        '&season_start=1&season_end=-1&pos%5B%5D=QB&pos%5B%5D=WR&pos%5B%5D=RB'
        '&pos%5B%5D=TE&is_starter=E&game_type=R&career_game_num_min=1'
        '&career_game_num_max=400&qb_start_num_min=1&qb_start_num_max=400'
        '&game_num_min=0&game_num_max=99&week_num_min=0&week_num_max=99'
        '&c5val=1.0&order_by=fantasy_points'
        f'&offset={page_off}'
    )

    game_scrape = GameScraper(url)
    df = game_scrape.create_df(col_list, int(counter))
    db_maker = DatabaseMaker(df)
    db_maker.create_db()

    config_parser.set('SETTINGS', 'offset', str(int(page_off) + 100))
    config_parser.set('SETTINGS', 'db_counter', str(int(counter) + 100))
    with open('config.ini', 'w') as configfile:
        config_parser.write(configfile)

    print(f'PAGE OFFSET: {page_off}')
    print(f'DB COUNTER: {counter}')

    time.sleep(10)
