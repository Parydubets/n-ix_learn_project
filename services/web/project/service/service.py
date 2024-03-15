from ..models import *
from sqlalchemy import desc
from math import ceil
from flask import send_from_directory, current_app
import os
from re import match, search

kwargs_pool = ["name", "release_date", "description", "rating", "poster",
                   "user_id", "genres", "director"]

def get_item_with_id(item, id):
    try:
        res = item.query.where(item.id == id).first()
    except:
        return None
    if res is not None:
        return res
    else:
        return None


def delete_item_with_id(item, id):
    item = item.query.filter_by(id=id).first()
    db.session.delete(item)
    db.session.commit()
    return item


def check_or_add_director(director_name):
    first_name, last_name = director_name.split(" ")
    if Director.query.where(Director.first_name == first_name).where(Director.last_name == last_name).first() is None:
        id = db.session.query(Director).order_by(Director.id.desc()).first().id
        director = Director(id=id+1,first_name=first_name, last_name=last_name, date_of_birth="2020-03-03")
        db.session.add(director)
        db.session.commit()
    director = Director.query.where(Director.first_name == first_name).where(Director.last_name == last_name).first()
    return director


def check_film_fileds(**kwargs):
    errors = []
    for arg in kwargs:
        if arg not in kwargs_pool:
            errors.append("Unknown film parameter <{}>".format(arg))
    keys = kwargs.keys()
    if "name" in keys and (len(kwargs["name"])>100 or len(kwargs["name"])<1):
        errors.append("Movie name lenght must be between 1 and 100 characters")
    if "poster" in keys and (search("([A-Za-z0-9])+(\.jpg|\.png)", kwargs["poster"]) is None):
        errors.append("Not a valid filename for poster")
    if "release_date" in keys and (search("[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9]", kwargs["release_date"]) is None):
        errors.append("Valid date format is yyyy-mm-dd")
    if "description" in keys:
        if len(kwargs["description"]) > 1000 or len(kwargs["description"]) < 10:
            errors.append("Movie description lenght must be between 10 and 1000 characters")
    if "rating" in keys and (float(kwargs["rating"])>10 or float(kwargs["rating"])<0):
        errors.append("Rating must be between 0 and 10")
    if "genres" in keys:
        genres = get_genres()
        kwargs["genres"] = kwargs["genres"].split(",")
        for item in kwargs["genres"]:
            if item not in genres:
                errors.append("No genre with name {}".format(item))
    if "user_id" in keys:
        user = get_item_with_id(User, kwargs["user_id"])
        if user is None:
            errors.append("No user with id {}".format( kwargs["user_id"]))

    return errors


def paginate_films(query, **kwargs):
    if "page" in kwargs:
        kwargs["page"] = int(kwargs["page"])
    else:
        kwargs["page"] = 1
    if "limit" in kwargs:
        kwargs["limit"] = int(kwargs["limit"])
    else:
        kwargs["limit"] = 10
    # pagination
    results = query.count()
    if results > kwargs["limit"]:
        query = query.paginate(page=kwargs["page"], per_page=kwargs["limit"])
    else:
        kwargs["page"] = 1
        query = query.all()
        if len(query) == 0:
            return 0, kwargs
    kwargs["pages"] = ceil(results / kwargs["limit"])
    return query, kwargs


def sort_films(base_query, **kwargs):
    if "sort" in kwargs:
        if kwargs["sort"] == "r-date":
            query = base_query.query.order_by(Film.release_date)
        elif kwargs["sort"] == "date":
            query = base_query.query.order_by(desc(Film.release_date))
        elif kwargs["sort"] == "r-rating":
            query = base_query.query.order_by(Film.rating)
        elif kwargs["sort"] == "rating":
            query = base_query.query.order_by(desc(Film.rating))
        else:
            return "Wrong sort parameter"
    else:
        query = base_query.query.order_by(Film.id)
    return query

def filter_films(query, **kwargs):
    if "date_from" in kwargs:
        query = query.filter(Film.release_date >= kwargs["date_from"])
    if "date_to" in kwargs:
        query = query.filter(Film.release_date <= kwargs["date_to"])

    if "genre" in kwargs:
        kwargs["genre"] = kwargs["genre"].lower()
        query = query.filter(Film.genres.any(name=kwargs["genre"]))

    if "director" in kwargs:
        try:
            first_name, last_name = kwargs["director"].split(" ")
        except:
            return {"message": "Enter director if format: <first-name> <last-name>"}
        director = db.session.query(Director).where(Director.first_name == first_name,
                                                    Director.last_name == last_name).first()
        if director is not None:
            query = query.filter(Film.director_id == director.id)
        else:
            return {"message":"Wrong director`s name"}
    return query


def get_result(query, **kwargs):
    query = films.dump(list(query))
    result = dict(**kwargs)
    result["films"] = query
    return result


def get_films(**kwargs):
    args_list = ["page", "limit", "sort", "genre", "director", "date_from", "date_to"]
    for item in kwargs:
        if item not in args_list:
            return {"message":"Wrong parameters"}
    base_query = Film

    #sorting
    query = sort_films(base_query, **kwargs)


    #filtering
    query = filter_films(query, **kwargs)


    #pagination kwargs
    query, kwargs = paginate_films(query, **kwargs)

    return get_result(query, **kwargs)


def get_film(id):
    movie = get_item_with_id(Film, id)
    if movie is None:
        return {"error": "No items with whis id"}
    result = film.dump(movie)
    return result

def get_film_img(id):
    movie = get_item_with_id(Film, id)
    if os.path.isfile("project/static/" + movie.poster) is False:
        return None
    return movie.poster


def add_film(**kwargs):
    director = check_or_add_director(kwargs["director"])
    user = get_item_with_id(User, kwargs["user_id"])
    genres = [Genre.query.where(Genre.name == item.lower()).first() for item in kwargs["genres"].split(",")]
    id = db.session.query(Film).order_by(Film.id.desc()).first().id
    obj = {
        "id": id+1,
        "name": kwargs["name"],
        "release_date": kwargs["release_date"],
        "description": kwargs["description"],
        "rating": kwargs["rating"],
        "poster": kwargs["poster"],
        "user_id": user.id,
        "director_id": director.id,
    }
    obj=Film(**obj)
    obj.genres.extend(genres)
    db.session.add(obj)
    db.session.commit()
    return film.dump(obj)


def update_film(id, **kwargs):
    errors = check_film_fileds(**kwargs)
    if len(errors) > 0:
        return errors
    keys = kwargs.keys()
    if "director" in keys:
        director = check_or_add_director(kwargs["director"])
        kwargs["director_id"] = director.id
        del kwargs["director"]
    movie = get_item_with_id(Film, id)
    if "genres" in keys:
        genres = [Genre.query.where(Genre.name == item.lower()).first() for item in kwargs["genres"].split(",")]
        movie.genres = genres
        del kwargs["genres"]
    for item in keys:
        if item in kwargs_pool:
            setattr(movie, item, kwargs[item])
    db.session.commit()
    return (film.dump(movie))

def delete_film(id):
    item = get_item_with_id(Film, id)
    if item is None:
        return {"error": "No items with whis id"}
    item = film.dump(item)
    try:
        delete_item_with_id(Film, id)
        return {"deleted":item}
    except:
        return {"error": "something went wrong"}




def get_Directors(page, limit=10):
    results = Director.query.count()
    result = Director.query.paginate(page=int(page), per_page=limit)
    return {"pages":ceil(results/limit), "page":page, "directors":directors.dump(result)}


def get_Director(id):
    result = director.dump(get_item_with_id(Director, id))
    return result


def get_genres():
    result = Genre.query.all()
    genres = [genre.name for genre in result]
    return genres