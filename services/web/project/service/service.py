"""
    The module with buisiness logic
"""
from math import ceil
import os
from re import search
from sqlalchemy import desc
from ..models import *
from flask import session, current_app
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash

film_kwargs_pool        = ["name", "release_date", "description", "rating",
                           "poster", "user_id", "genres", "director"]
director_kwargs_pool    = ["first_name", "last_name", "date_of_birth"]
args_list               = ["page", "limit", "sort", "genre", "director",
                           "date_from", "date_to"]


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


def get_item_with_filter(data, type, filter):
    query = type.query.filter(filter == data).first()
    if query is not None:
        return "item with {} = {} already exists".format(str(filter).split(".")[1], data)
    return ""

def delete_item_with_id(serialize, type, id):
    item = get_item_with_id(type, id)
    print(item)
    print(serialize.dump(item))
    if item is None:
        current_app.logger.warning("No items with id={}".format(id))
        return {"error": "No items with this id"}, 400
    try:
        db.session.delete(item)
        db.session.commit()
        item = serialize.dump(item)
        print(item)
        return {"deleted": item}
    except:
        current_app.logger.warning("Something went wrong")
        return {"error": "something went wrong"}, 400


def check_author(user):
    print(user.id, current_user.id, current_user.is_admin)
    if user.id == current_user.id or current_user.is_admin is True:
        return True
    return False


def check_director(director_name):
    first_name, last_name = director_name.split(" ")
    if Director.query.where(Director.first_name == first_name).\
            where(Director.last_name == last_name).first() is None:
        return "no director with this name"
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
    if "poster" in keys and (search(r"([A-Za-z0-9])+(\.jpg|\.png)", kwargs["poster"]) is None):
        errors.append("Not a valid filename for poster")
    if "release_date" in keys:
        if (search(r"^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$", kwargs["release_date"]) is None):
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


def check_filter_fileds(**kwargs):
    errors = []
    keys = kwargs.keys()
    for arg in kwargs:
        if arg == "sort":
            if kwargs[arg] not in ["date", "r-date", "rating", "r-rating"]:
                errors.append("wrong sort parameter")
        if arg == "genre":
            if kwargs[arg] not in get_genres():
                errors.append("no such genre")
        if arg == "director":
            if check_director(kwargs[arg]) == "no director with this name":
                errors.append("no director with this name")
        if arg == "date_from":
            if (search(r"^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$", kwargs["date_from"]) is None):
                errors.append("valid date format is yyyy-mm-dd")
        if arg == "date_to":
            if (search(r"^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$", kwargs["date_to"]) is None):
                errors.append("valid date format is yyyy-mm-dd")
    if "date_from" in kwargs and "date_to" in kwargs:
        if kwargs["date_from"] > kwargs["date_to"]:
            errors.append("date_from filter bigger than date_to")
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
        if (search(r"[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9]", kwargs["date_of_birth"]) is None):
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
            current_app.logger.warning("No films requested")
            return 0, kwargs
    kwargs["pages"] = ceil(results / kwargs["limit"])
    return query, kwargs
    return {"error": "no items with these parameters"}, kwargs


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
        first_name, last_name = kwargs["director"].split(" ")
        director = db.session.query(Director).where(Director.first_name == first_name,
                                                    Director.last_name == last_name).first()
    return query


def get_result(query, **kwargs):
    current_app.logger.warning(query)
    query = films.dump(list(query))
    current_app.logger.warning(query)
    for item in query:
        if item["director"] is None:
            item["director"] = "Unknown"
    result = dict(**kwargs)
    result["films"] = query
    return result


def get_films(**kwargs):
    for item in kwargs:
        if item not in args_list:
            current_app.logger.warning("Wrong parameters")
            return {"message":"Wrong parameters"}, 400
    errors = check_filter_fileds(**kwargs)
    if len(errors)>0:
        current_app.logger.warning("errors: {}".format(errors))
        return errors, 400
    base_query = Film
    #sorting
    query = sort_films(base_query, **kwargs)

    #filtering
    query = filter_films(query, **kwargs)
    current_app.logger.warning(query)

    #pagination kwargs
    query, kwargs = paginate_films(query, **kwargs)
    if query == 0:
        return query, 400
    return get_result(query, **kwargs)


def get_film(id):
    movie = get_item_with_id(Film, id)
    if movie is None:
        current_app.logger.warning("No films with id={}".format(id))
        return {"error": "No items with whis id"}, 400
    result = film.dump(movie)
    return result

def get_film_img(id):
    movie = get_item_with_id(Film, id)
    return movie.poster


def add_film(**kwargs):
    #validate_fields
    errors = check_film_fileds(**kwargs)

    if "description" not in kwargs:
        kwargs["description"] = ""
    if len(kwargs) != 8:
        errors.append("check parameters again")

    check_name = get_item_with_filter(kwargs["name"], Film, Film.name)
    if len(check_name)>0:
        errors.append(check_name)

    #check director
    director = check_director(kwargs["director"])
    if isinstance(director, str):
        errors.append(director)

    if len(errors) > 0:
        current_app.logger.warning("errors: {}".format(errors))
        return {"errors": errors}, 400

    user = get_item_with_id(User, kwargs["user_id"])
    genres = get_genres_list(kwargs["genres"])
    id = get_last_id(Film)
    obj = {
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
    current_app.logger.info("Added the film")
    return {"film": film.dump(obj)}


def update_film(id, **kwargs):
    errors = check_film_fileds(**kwargs)
    keys = kwargs.keys()
    if "director" in keys:
        director = check_director(kwargs["director"])
        if isinstance(director, str):
            errors.append(director)
        kwargs["director"] = director
    print(kwargs)
    movie = get_item_with_id(Film, id)
    check_author(movie.user)

    if check_author(movie.user) is False:
        errors.append("Not an author or admin")
    if movie is None:
        errors.append("No items with this id")

    if len(errors) > 0:
        current_app.logger.warning("errors: {}".format(errors))
        return {"errors": errors}, 400
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
    movie = get_item_with_id(Film, id)
    if check_author(movie.user) is False:
        current_app.logger.warning("user with id={} is not an author or admin".format(current_user.id))
        return {"error": "Not an author or admin"}, 400
    return delete_item_with_id(film, Film, id)


def get_directors(page, limit=10):
    results = Director.query.count()
    if results < 1:
        current_app.logger.warning("No directors in db")
        return {"error": "no directors found"}, 400
    result = Director.query.order_by(Director.id).paginate(page=int(page), per_page=limit)
    return {"pages":ceil(results/limit), "page":page, "directors":directors.dump(result)}


def get_director(id):
    result = get_item_with_id(Director, id)
    if result is None:
        current_app.logger.warning("No director with id={}".format(id))
        return {"error": "no directors with this id"}, 400
    result = director.dump(result)
    return result


def create_director(**kwargs):
    errors = check_director_fileds(**kwargs)
    error = get_item_with_filter(kwargs["first_name"], Director, Director.first_name)
    if len(error)>0:
        errors.append(error)
    error = get_item_with_filter(kwargs["last_name"], Director, Director.last_name)
    if len(error)>0:
        errors.append(error)
    if len(errors)>0:
        current_app.logger.warning("errors: {}".format(errors))
        return {"errors": errors}, 400

    obj = {
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
        current_app.logger.warning("No director with id={}".format(id))
        return {"error": "No items with this id"}, 400
    errors = check_director_fileds(**kwargs)
    if len(errors) > 0:
        current_app.logger.warning("errors: {}".format(errors))
        return {"errors": errors}, 400

    keys = kwargs.keys()
    for item in keys:
        setattr(director_update, item, kwargs[item])
    db.session.commit()
    return {"updated dicrector": director.dump(director_update)}


def delete_director(id):
    return delete_item_with_id(director, Director, id)


def get_genres():
    """
    Returns list of genres from db
    @return: genres
    @rtype: list
    """
    result = Genre.query.all()
    if result is None:
        current_app.logger.warning("No genres in database")
        return []
    genres = [genre.name for genre in result]
    return genres


def get_genres_list(items):
    """
    Returns film genres as list

    @param items:
    @type string:
    @return: genres
    @rtype: list
    """
    return [Genre.query.where(Genre.name == item.lower()).first()
            for item in items.split(",")]


def signup(username, password):
    with current_app.app_context():
        new_user = User(username=username)
        new_user.password_hash = password

        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id
        return new_user.to_dict()


def get_user_data():
    usr = get_item_with_id(User, current_user.id)
    if usr is not None:
        return {"user:":models.user.dump(usr)}


def set_user_password(password):
    current_user.password = generate_password_hash(password)
    usr = get_item_with_id(User, current_user.id)
    usr.pasword = generate_password_hash(password)
    db.session.commit()
