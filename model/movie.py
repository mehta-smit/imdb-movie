from sqlalchemy import Column, Index

from constant.common_constant import ACTIVE
from .base import db
from .session import session
from .utils import PRIMARY_KEY, CREATED_AT, MODIFIED_AT, IS_DELETED


class Movie(db.Model):
    __tabelname__ = 'movie'

    id = PRIMARY_KEY.copy()
    name = Column(db.String(255))
    popularity = Column('99popularity', db.Float)
    director = Column(db.String(255))
    genre = Column(db.String(255))
    imdb_score = Column(db.Float)
    created_at = CREATED_AT.copy()
    modified_at = MODIFIED_AT.copy()
    is_deleted = IS_DELETED.copy()

    def add(self):
        imdb_movie = Movie()
        imdb_movie.Name = self.name
        imdb_movie.popularity = self.popularity
        imdb_movie.director = self.director
        imdb_movie.genre = self.genre
        imdb_movie.imdb_score = self.imdb_score

        session.add(imdb_movie)
        session.flush()
        session.commit()
        return True

    def get_all_movie(self):
        imdb_movie_list = session.query(Movie).filter_by(
            Movie.is_deleted == ACTIVE
        ).all()

        return imdb_movie_list
