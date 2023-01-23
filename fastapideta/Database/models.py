from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from . import database as db

class Game(db.Base):
    __tablename__ = 'game'
    g_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    g_name = Column(String(40), primary_key=True, nullable=False)
    g_type = Column(String(40), nullable=False)
    TOURNAMENT = relationship('Tournament', back_populates='GAME', cascade="all, delete-orphan", single_parent=True, passive_deletes=True)

class User(db.Base):
    __tablename__ = 'user'
    usn = Column(String(10), primary_key=True, nullable=False)
    name = Column(String(40), nullable=False)
    email = Column(String(40), nullable=False, primary_key=True)
    dob = Column(Date, nullable=False)
    password = Column(String(80), nullable=False)
    role = Column(String(10), nullable=False, default='player')
    TOURNAMENT = relationship('Tournament', back_populates='USER', cascade="all, delete-orphan", single_parent=True, passive_deletes=True)
    REGISTRATION = relationship('Registration', back_populates='USER', cascade="all, delete-orphan", single_parent=True, passive_deletes=True)

class Tournament(db.Base):
    __tablename__ = 'tournament'
    t_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    t_name = Column(String(40), nullable=False)
    t_desc = Column(String(500), nullable=False)
    t_date = Column(Date, nullable=False)
    last_reg_date = Column(Date, nullable=False)
    coach = Column(String(10), ForeignKey('user.usn', ondelete='CASCADE'), nullable=False)
    game = Column(Integer, ForeignKey('game.g_id', ondelete='CASCADE'), nullable=False)
    USER = relationship('User', back_populates='TOURNAMENT')
    GAME = relationship('Game', back_populates='TOURNAMENT')
    REGISTRATION = relationship('Registration', back_populates='TOURNAMENT', cascade="all, delete-orphan", single_parent=True, passive_deletes=True)

class Registration(db.Base):
    __tablename__ = 'registration'
    r_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    r_tour = Column(Integer, ForeignKey('tournament.t_id', ondelete='CASCADE'), nullable=False)
    r_player = Column(String(10), ForeignKey('user.usn', ondelete='CASCADE'), nullable=False)
    r_date = Column(Date, nullable=False)
    USER = relationship('User', back_populates='REGISTRATION')
    TOURNAMENT = relationship('Tournament', back_populates='REGISTRATION')
