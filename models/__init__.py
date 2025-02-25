from .book_form import BookForm, BOOK_GENRES, BOOK_STATUSES
from .movie_form import MovieForm, MOVIE_GENRES, MOVIE_TYPES, MOVIE_STATUSES
from .contact_form import ContactForm, CITIES
from .base import BaseManager
from .book_list import BookList
from .movie_list import MovieList
from .contact_list import ContactList

# Импортируем менеджеры из новых файлов
from .book_model import BookManager
from .movie_model import MovieManager
from .contact_model import ContactManager

__all__ = [
    'BookForm', 'BookManager', 'BookList', 'BOOK_GENRES', 'BOOK_STATUSES',
    'MovieForm', 'MovieManager', 'MovieList', 'MOVIE_GENRES', 'MOVIE_TYPES', 'MOVIE_STATUSES',
    'ContactForm', 'ContactManager', 'ContactList', 'CITIES'
] 