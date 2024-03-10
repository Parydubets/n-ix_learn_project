from ..models import *
from sqlalchemy import desc
from math import ceil

def get_Films(**kwargs):
    page = 1
    limit = 10

    #pagination kwargs
    if "page" in kwargs:
        kwargs["page"] = int(kwargs["page"])
        page = kwargs["page"]
    else:
        kwargs["page"] = 1
    if "limit" in kwargs:
        kwargs["limit"] = int(kwargs["limit"])
        limit = int(kwargs["limit"])

    base_query = Film

    #sorting
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
        query = base_query.query.order_by(Film.film_id)


    #filtering
    if "date_from" in kwargs:
        query = query.filter(Film.release_date >= kwargs["date_from"])
    if "date_to" in kwargs:
        query = query.filter(Film.release_date <= kwargs["date_to"])

    if "genre" in kwargs:
        query = query.filter(Film.genres.any(name=kwargs["genre"]))

    if "director" in kwargs:
        first_name, last_name = kwargs["director"].split(" ")
        director = db.session.query(Director).where(Director.first_name == first_name, Director.last_name==last_name).first()
        if director is not None:
            query = query.filter(Film.directors_director_id == director.director_id)
        else:
            return {"message":"Wrong director`s name"}

    # pagination
    results = query.count()
    if results > limit:
        query = query.paginate(page=page, per_page=limit)
    else:
        kwargs["page"] = 1
        query = query.all()

    pages = ceil(results/limit)
    query = films.dump(list(query))
    result = dict(**kwargs)
    result["pages"] = pages
    result["films"] = query
    return result


def get_Film(film_id):
    movie = Film.query.where(Film.film_id==film_id).first()
    result = film.dump(movie)
    result['genres'] = [item.name for item in movie.genres]
    return result


def get_Directors(page, limit=10):
    result = Director.query.paginate(page=int(page), per_page=limit)
    return directors.dump(result)


def get_Director(director_id):
    result = director.dump(Film.query.where(Director.director_id==director_id).scalar())
    return result
