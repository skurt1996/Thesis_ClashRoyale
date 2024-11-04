from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, unique=True)
    name = Column(String)

    def __init__(self, location_id, name):
        self.location_id = location_id
        self.name = name


class Clan(Base):
    __tablename__ = "clans"
    id = Column(Integer, primary_key=True)
    tag = Column(String, unique=True)
    last_retrieved = Column(DateTime)

    def __init__(self, tag, last_retrieved=None):
        self.tag = tag
        self.last_retrieved = last_retrieved or datetime.utcnow()


class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    tag = Column(String)
    last_retrieved = Column(DateTime)

    def __init__(self, tag, last_retrieved=None):
        self.tag = tag
        self.last_retrieved = last_retrieved or datetime.utcnow()


class Battle(Base):
    __tablename__ = 'battles'
    id = Column(Integer, primary_key=True)
    battle_time = Column(DateTime)
    game_mode = Column(String)
    p1_tag = Column(String)
    p1_trophies = Column(Integer)
    p1_best_trophies = Column(Integer)
    p1_wins = Column(Integer)
    p1_losses = Column(Integer)
    p1_battle_count = Column(Integer)
    p1_crowns = Column(Integer)
    p1_elixir_leaked = Column(Float)
    p1_cards = Column(JSON)
    p1_support_cards = Column(JSON)
    p2_tag = Column(String)
    p2_trophies = Column(Integer)
    p2_best_trophies = Column(Integer)
    p2_wins = Column(Integer)
    p2_losses = Column(Integer)
    p2_battle_count = Column(Integer)
    p2_crowns = Column(Integer)
    p2_elixir_leaked = Column(Float)
    p2_cards = Column(JSON)
    p2_support_cards = Column(JSON)

    def __init__(self, battle_time, game_mode, p1_tag, p1_trophies, p1_best_trophies,
                 p1_wins, p1_losses, p1_battle_count, p1_crowns, p1_elixir_leaked,
                 p1_cards, p1_support_cards, p2_tag, p2_trophies, p2_best_trophies,
                 p2_wins, p2_losses, p2_battle_count, p2_crowns, p2_elixir_leaked,
                 p2_cards, p2_support_cards):
        self.battle_time = battle_time
        self.game_mode = game_mode
        self.p1_tag = p1_tag
        self.p1_trophies = p1_trophies
        self.p1_best_trophies = p1_best_trophies
        self.p1_wins = p1_wins
        self.p1_losses = p1_losses
        self.p1_battle_count = p1_battle_count
        self.p1_crowns = p1_crowns
        self.p1_elixir_leaked = p1_elixir_leaked
        self.p1_cards = p1_cards
        self.p1_support_cards = p1_support_cards
        self.p2_tag = p2_tag
        self.p2_trophies = p2_trophies
        self.p2_best_trophies = p2_best_trophies
        self.p2_wins = p2_wins
        self.p2_losses = p2_losses
        self.p2_battle_count = p2_battle_count
        self.p2_crowns = p2_crowns
        self.p2_elixir_leaked = p2_elixir_leaked
        self.p2_cards = p2_cards
        self.p2_support_cards = p2_support_cards


# Create the engine
engine = create_engine('sqlite:///clash_royale.db?timeout=10', echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
