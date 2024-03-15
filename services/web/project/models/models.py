from sqlalchemy import Column, Integer, Float, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields

"""
    The SQLAlchemy models
"""

db = SQLAlchemy()


association_table = db.Table('film_genre',
                             db.Column('film_id', db.Integer,
                                       db.ForeignKey('films.id')),
                             db.Column('genre_id', db.Integer,
                                       db.ForeignKey('genres.id'))
                             )
class Director(db.Model):
    __tablename__ = "directors"

    id     = Column(Integer, primary_key=True)
    first_name      = Column(String, nullable=False)
    last_name       = Column(String, nullable=False)
    date_of_birth   = Column(Date, nullable=False)
    films = db.relationship('Film', backref='director')



class User(db.Model):
    __tablename__ = "users"

    id     = Column(Integer, primary_key=True)
    first_name  = Column(String, nullable=False)
    last_name   = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    email       = Column(String, nullable=False)
    password    = Column(String, nullable=False)
    phone       = Column(String, nullable=False)
    is_admin    = Column(Boolean, nullable=False)
    films = db.relationship('Film', backref='user')

class Film(db.Model):
    __tablename__ = "films"

    id         = Column(Integer, primary_key=True)
    name            = Column(String, nullable=False)
    release_date    = Column(Date, nullable=False)
    description     = Column(String, nullable=True)
    rating          = Column(Float, nullable=False)
    poster          = Column(String, nullable=False)
    user_id   = mapped_column(ForeignKey("users.id"))
    director_id   = mapped_column(ForeignKey("directors.id"))
    genres = db.relationship(
        "Genre", secondary=association_table, backref=db.backref('films'), cascade='save-update')

class Genre(db.Model):
    __tablename__ = "genres"

    id    = Column(Integer, primary_key=True)
    name        = Column(String, nullable=False)
"""
    The Marshmallow schemas
"""

ma = Marshmallow()

class UsersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class UsersSmallSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name")

class GenresSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Genre

class GenresSmallSchema(ma.SQLAlchemyAutoSchema):
    name = fields.Pluck(GenresSchema, 'name', many=True)

class DirectorsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Director

class DirectorsSmallSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Director
        fields = ("first_name", "last_name")

class FilmsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Film
        include_fk = True

    film_id = fields.Int()
    name = fields.Str()
    release_date = fields.Str()
    description = fields.Str()
    rating = fields.Float()
    poster = fields.Str()
    genres = fields.Pluck("self", "name", many=True)
    user = ma.Nested(UsersSmallSchema)
    director = ma.Nested(DirectorsSmallSchema)


film = FilmsSchema(exclude=("user_id", "director_id"))
films = FilmsSchema(many=True, exclude=("user_id", "director_id"))

director = DirectorsSchema()
directors = DirectorsSchema(many=True)

genre = GenresSchema()
genres = GenresSmallSchema(many=True)
