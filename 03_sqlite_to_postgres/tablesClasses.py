import uuid
from dataclasses import dataclass, field
from datetime import datetime


TABLES = {
    'film_work': 'FilmWork',
    'genre': 'Genre',
    'person': 'Person',
    'person_film_wok': 'PersonFilmWork',
    'genre_film_work': 'GenreFilmWork',
}

FIELDS = {
    'film_work': [
        'title',
        'description',
        'creation_date',
        'type',
        'rating',
        'id',
    ],
    'genre': [],
}


@dataclass
class FilmWork:
    title: str
    description: str
    creation_date: datetime
    type: str
    rating: float = field(default=0.0)
    id: uuid.UUID = field(default_factory=uuid.uuid4)




#
#
# movie = Movie(title='movie', description='new movie', rating=0.0)
# print(movie)
# # Movie(title='movie', description='new movie', rating=0.0, id=UUID('6fe77164-1dfe-470d-a32d-071973759539'))