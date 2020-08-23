import time

from configparser import ConfigParser

from pfr_scraper import GameScraper, DatabaseMaker

page_off = 0

year1 = 1980
year2 = 2020
col_list = [
    'player_id', 'player', 'year_id', 'draft_round', 'draft_pick', 'pos',
    'draft_age', 'college_id'
]

while int(page_off) < 11400:
    config_parser = ConfigParser()
    config_parser.read('config.ini')
    page_off = config_parser.get('SETTINGS', 'draft_offset')
    counter = config_parser.get('SETTINGS', 'draft_db_counter')

    url = (
        'https://www.pro-football-reference.com/play-index/draft-finder.cgi?'
        f'request=1&year_min={year1}&year_max={year2}&pick_type=overall&pos%5B'
        '%5D=qb&pos%5B%5D=rb&pos%5B%5D=wr&pos%5B%5D=te&pos%5B%5D=e&pos%5B%5D=t'
        '&pos%5B%5D=g&pos%5B%5D=c&pos%5B%5D=ol&pos%5B%5D=dt&pos%5B%5D=de&pos'
        '%5B%5D=dl&pos%5B%5D=ilb&pos%5B%5D=olb&pos%5B%5D=lb&pos%5B%5D=cb&pos'
        '%5B%5D=s&pos%5B%5D=db&pos%5B%5D=k&pos%5B%5D=p&conference=any'
        f'&show=all&order_by=default&offset={page_off}'
    )

    game_scrape = GameScraper(url)
    df = game_scrape.create_draft_df(col_list, int(counter))
    db_maker = DatabaseMaker(df)
    db_maker.create_draft_db()

    config_parser.set('SETTINGS', 'draft_offset', str(int(page_off) + 300))
    config_parser.set('SETTINGS', 'draft_db_counter', str(int(counter) + 300))
    with open('config.ini', 'w') as configfile:
        config_parser.write(configfile)

    print(f'PAGE OFFSET: {page_off}')
    print(f'DB COUNTER: {counter}')

    time.sleep(10)
