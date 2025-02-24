from .book_form import BookForm, BOOK_GENRES, BOOK_STATUSES
from .movie_form import MovieForm, MOVIE_GENRES, MOVIE_TYPES, MOVIE_STATUSES
from .contact_form import ContactForm, CITIES
from .base import BaseManager
from .book_list import BookList
from .movie_list import MovieList
from .contact_list import ContactList

# Создаем классы менеджеров
class BookManager(BaseManager):
    def __init__(self):
        super().__init__("books.json")
    
    def add_book(self, book):
        self.add_item(book)
    
    def update_book(self, index, book):
        self.update_item(index, book)
    
    def delete_book(self, index):
        self.delete_item(index)
    
    def get_books(self):
        return self.get_items()

class MovieManager(BaseManager):
    def __init__(self):
        super().__init__("movies.json")
    
    def add_movie(self, movie):
        self.add_item(movie)
    
    def update_movie(self, index, movie):
        self.update_item(index, movie)
    
    def delete_movie(self, index):
        self.delete_item(index)
    
    def get_movies(self):
        return self.get_items()

class ContactManager(BaseManager):
    def __init__(self):
        super().__init__("contacts.json")
    
    def add_contact(self, contact):
        self.add_item(contact)
    
    def update_contact(self, index, contact):
        self.update_item(index, contact)
    
    def delete_contact(self, index):
        self.delete_item(index)
    
    def get_contacts(self):
        return self.get_items()

__all__ = [
    'BookForm', 'BookManager', 'BookList', 'BOOK_GENRES', 'BOOK_STATUSES',
    'MovieForm', 'MovieManager', 'MovieList', 'MOVIE_GENRES', 'MOVIE_TYPES', 'MOVIE_STATUSES',
    'ContactForm', 'ContactManager', 'ContactList', 'CITIES'
] 