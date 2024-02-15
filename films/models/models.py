from sqlalchemy import Column, Integer, Numeric, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Genre(db.Model):
    __tablename__ = "genres"

    genre_id    = db.Column(Integer, primary_key=True)
    name        = db.Column(String, nullable=False)


class Director(db.Model):
    __tablename__ = "directors"

    director_id     = Column(Integer, primary_key=True)
    first_name      = Column(String, nullable=False)
    last_name       = Column(String, nullable=False)
    date_of_birth   = Column(Date, nullable=False)
    films           = relationship('Film', backref='users')


class User(db.Model):
    __tablename__ = "users"

    user_id     = Column(Integer, primary_key=True)
    first_name  = Column(String, nullable=False)
    last_name   = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    email       = Column(String, nullable=False)
    password    = Column(String, nullable=False)
    phone       = Column(String, nullable=False)
    is_admin    = Column(Boolean, nullable=False)
    films = relationship('Film', backref='users')


class Film(db.Model):
    __tablename__ = "films"

    film_id         = Column(Integer, primary_key=True)
    name            = Column(String, nullable=False)
    release_date    = Column(Date, nullable=False)
    description     = Column(String, nullable=True)
    rating          = Column(Numeric, nullable=False)
    poster          = Column(String, nullable=False)
    users_user_id   = Column(Integer, ForeignKey('users.user_id'))
    directors_director_id = Column(Integer, ForeignKey('directors.director_id'))
