
from models.user import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database/bot_db.sqlite')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)