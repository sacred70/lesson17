# app.py

from flask import request
from flask_restx import Api, Resource
from config import app, db
from models import MovieSchema, Movie, DirectorSchema, Director, GenreSchema, Genre


#  класс Api из flask_restx
api = Api(app)
#  создаем namespace
movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')

#  Создаем экземпляр класса
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@movie_ns.route('/')
class MovieView(Resource):
    #  get запрос
    def get(self):
        movie_query = db.session.query(Movie)
        director_id = request.args.get('director_id')
        if director_id is not None:
            movie_query = movie_query.filter(Movie.director_id == director_id)
        genre_id = request.args.get('genre_id')
        if genre_id is not None:
            movie_query = movie_query.filter(Movie.genre_id == genre_id)
        return movies_schema.dump(movie_query.all()), 200

    #  post запрос
    def post(self):
        reg_json = request.json
        new_movies = Movie(**reg_json)
        with db.session.begin():
            db.session.add(new_movies)
        return "", 201


# запрос по id
@movie_ns.route('/<int:uid>')
class MovieView(Resource):
    #  get запрос
    def get(self, uid:int):
        # если запрос верный
        try:
            movie = db.session.query(Movie).get(uid)
            return  movie_schema.dump(movie), 200
        #  если запрос не верный
        except Exception:
            return "", 404

    #  put запрос
    def put(self, uid: int):
        try:
            movie = Movie.query.get(uid)
            req_json = request.json
            # movie.id = req_json.get('id') не нужно
            movie.title = req_json.get('title')
            movie.description = req_json.get('description')
            movie.trailer = req_json.get('trailer')
            movie.year = req_json.get('year')
            movie.rating = req_json.get('rating')
            movie.genre_id = req_json.get('genre_id')
            movie.director_id = req_json.get('director_id')
            db.session.add(movie)
            db.session.commit()
            return "", 204
        except Exception:
            return "", 400

        #  del запрос
    def delete(self, uid: int):
        movie = Movie.query.get(uid)
        db.session.delete(movie)
        db.session.commit()
        return "", 204


@director_ns.route('/')
class DirectorsView(Resource):
    #  get запрос
    def get(self):
        all_director = Director.query.all()
        return directors_schema.dump(all_director), 200

    #  post запрос
    def post(self):
        req_json = request.json
        new_director = Director(**req_json)
        with db.session.begin():
            db.session.add(new_director)
        return "", 201


@director_ns.route('/<int:uid>')
class DirectorView(Resource):
    #  get запрос
    def get(self, uid: int):
        try:
            director = Director.query.get(uid)
            return director_schema.dump(director), 200
        except Exception:
            return "", 404

    #  put запрос
    def put(self, uid: int):
        try:
            director = Director.query.get(uid)
            req_json = request.json
            # director.id = req_json.get('id')
            director.name = req_json.get('name')
            db.session.add(director)
            db.session.commit()
            return "", 204
        except Exception:
            return "", 404

    #  del запрос
    def delete(self, uid: int):
        director = Director.query.get(uid)
        db.session.delete(director)
        db.session.commit()
        return "", 204


@genre_ns.route('/')
class GenresView(Resource):
    #  get запрос
    def get(self):
        all_genre = Genre.query.all()
        return genres_schema.dump(all_genre), 200

    #  post запрос
    def post(self):
        req_json = request.json
        new_genre = Genre(**req_json)
        with db.session.begin():
            db.session.add(new_genre)
        return "", 201


@genre_ns.route('/<int:uid>')
class GenreView(Resource):
    #  get запрос *
    def get(self, uid: int):
        try:
            genre = Genre.query.get(uid)
            return genre_schema.dump(genre), 200
        except Exception:
            return "", 404

    #  put запрос*
    def put(self, uid: int):
        try:
            genre = Genre.query.get(uid)
            req_json = request.json
            genre.name = req_json.get('name')
            db.session.add(genre)
            db.session.commit()
            return "", 204
        except Exception:
            return "", 404

    #  del запрос
    def delete(self, uid: int):
        genre = Genre.query.get(uid)
        db.session.delete(genre)
        db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run(debug=True)
