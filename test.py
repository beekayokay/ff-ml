from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class GameLog(Base):
    __tablename__ = 'gamelog'

    id = Column('id', Integer, primary_key=True)
    player_id = Column('player_id', String)


engine = create_engine('sqlite:///test.db', echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

session = Session()

# gamelog = GameLog()
# gamelog.id = 0
# gamelog.player_id = 'tombrady20204'

# session.add(gamelog)
# session.commit()

gamelogs = session.query(GameLog).all()
for log in gamelogs:
    print(log)

session.close()
