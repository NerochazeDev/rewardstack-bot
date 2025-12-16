from sqlalchemy import Column, Integer, Float, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database (stored locally)
engine = create_engine("sqlite:///rewardstack.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"
    telegram_id = Column(Integer, primary_key=True)
    username = Column(String)
    trc20_wallet = Column(String)
    balance = Column(Float, default=0)
    plan_cost = Column(Integer, default=0)
    daily_reward = Column(Float, default=5)
    min_withdraw = Column(Float, default=50)
    last_credit = Column(String)

# Create tables
Base.metadata.create_all(engine)
