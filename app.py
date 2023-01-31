# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from config import app, db
from models import MovieSchema, Movie, DirectorSchema, Director, GenreSchema, Genre


api = Api(app)
# создаем namespace
movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace('genres')

# Создаем экземпляр класса
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)





if __name__ == '__main__':
    app.run(debug=True)
