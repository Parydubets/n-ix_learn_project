"""
    The module with buisiness logic
"""
from ..models import *
from sqlalchemy import desc
from math import ceil
from flask import send_from_directory, current_app
import os
from re import match, search

film_kwargs_pool = ["name", "release_date", "description", "rating", "poster",
                   "user_id", "genres", "director"]
director_kwargs_pool = ["first_name", "last_name", "date_of_birth"]

def get_last_id(model):
    return db.session.query(model).order_by(model.id.desc()).first().id


def get_item_with_id(item, id):
    try:
        res = item.query.where(item.id == id).first()
    except:
        return None
    if res is not None:
        return res
    else:
        return None


def delete_item_with_id(serialize, type, id):
    item = get_item_with_id(type, id)
    print(item)
    print(serialize.dump(item))
    if item is None:
        return {"error": "No items with this id"}
    try:
        db.session.delete(item)
        db.session.commit()
        item = serialize.dump(item)
        print(item)
        return {"deleted": item}
    except:
        return {"error": "something went wrong"}




def check_director(director_name):
    first_name, last_name = director_name.split(" ")
    if Director.query.where(Director.first_name == first_name).\
            where(Director.last_name == last_name).first() is None:
        return {"error": "add director first"}
    director = Director.query.where(Director.first_name == first_name).\
        where(Director.last_name == last_name).first()
    return director


def check_film_fileds(**kwargs):
    errors = []
    for arg in kwargs:
        if arg not in film_kwargs_pool:
            errors.append("Unknown film parameter <{}>".format(arg))
    keys = kwargs.keys()
    if "name" in keys and (len(kwargs["name"])>100 or len(kwargs["name"])<1):
        errors.append("Movie name lenght must be between 1 and 100 characters")
    if "poster" in keys and (search("([A-Za-z0-9])+(\.jpg|\.png)", kwargs["poster"]) is None):
        errors.append("Not a valid filename for poster")
    if "release_date" in keys:
        if (search("[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9]", kwargs["release_date"]) is None):
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


def check_director_fileds(**kwargs):
    errors = []
    keys = kwargs.keys()
    for arg in kwargs:
        if arg not in director_kwargs_pool:
            errors.append("Unknown film parameter <{}>".format(arg))
    if "first_name" in keys and (len(kwargs["first_name"])>50 or len(kwargs["first_name"])<1):
        errors.append("Director`s name lenght must be between 1 and 50 characters")
    if "last_name" in keys and (len(kwargs["last_name"])>50 or len(kwargs["last_name"])<1):
        errors.append("Director`s name lenght must be between 1 and 50 characters")
    if "date_of_birth" in keys:
        if (search("[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9]", kwargs["date_of_birth"]) is None):
            errors.append("Valid date format is yyyy-mm-dd")
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
    for item in query:
        if item["director"] is None:
            item["director"] = "Unknown"
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
    errors = check_film_fileds(**kwargs)
    if "description" not in kwargs:
        kwargs["description"] = ""
    if len(errors) > 0:
        return {"errors": errors}
    if len(kwargs) != 8:
        return {"errors": "check parameters again"}
    director = check_director(kwargs["director"])
    if type(director) == type({}):
        return director
    user = get_item_with_id(User, kwargs["user_id"])
    genres = get_genres_list(kwargs["genres"])
    id = get_last_id(Film)
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
    return {"film": film.dump(obj)}


def update_film(id, **kwargs):
    errors = check_film_fileds(**kwargs)
    if len(errors) > 0:
        return {"errors": errors}
    keys = kwargs.keys()
    if "director" in keys:
        director = check_director(kwargs["director"])
        if type(director) == type({}):
            return director
        kwargs["director"] = director
    print(kwargs)
    movie = get_item_with_id(Film, id)
    if movie is None:
        return {"error": "No items with this id"}
    if "genres" in keys:
        genres = get_genres_list(kwargs["genres"])
        movie.genres = genres
        del kwargs["genres"]
    for item in keys:
        if item in film_kwargs_pool:
            setattr(movie, item, kwargs[item])
    db.session.commit()
    return {"film": film.dump(movie)}


def delete_film(id):
    return delete_item_with_id(film, Film, id)


def get_Directors(page, limit=10):
    results = Director.query.count()
    result = Director.query.order_by(Director.id).paginate(page=int(page), per_page=limit)
    return {"pages":ceil(results/limit), "page":page, "directors":directors.dump(result)}


def get_Director(id):
    result = director.dump(get_item_with_id(Director, id))
    return result


def create_director(**kwargs):
    errors = check_director_fileds(**kwargs)
    if len(errors)>0:
        return {"errors": errors}
    id = get_last_id(Director)
    obj = {
        "id": id+1,
        "first_name": kwargs["first_name"],
        "last_name": kwargs["last_name"],
        "date_of_birth": kwargs["date_of_birth"]
    }
    obj = Director(**obj)
    db.session.add(obj)
    db.session.commit()
    return {"director": director.dump(obj)}


def update_director(id, **kwargs):
    director_update = get_item_with_id(Director, id)
    if director_update is None:
        return {"error": "No items with this id"}
    errors = check_director_fileds(**kwargs)
    if len(errors) > 0:
        return {"errors": errors}

    keys = kwargs.keys()
    for item in keys:
        setattr(director_update, item, kwargs[item])
    db.session.commit()
    return {"updated dicrector": director.dump(director_update)}


def delete_director(id):
    return delete_item_with_id(director, Director, id)


def get_genres():
    result = Genre.query.all()
    genres = [genre.name for genre in result]
    return genres


def get_genres_list(genres):
    return [Genre.query.where(Genre.name == item.lower()).first()
            for item in genres.split(",")]
