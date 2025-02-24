from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivy.core.window import Window

# Устанавливаем начальный размер окна
Window.size = (800, 700)

from models import (
    BookForm, BookManager, BookList,
    MovieForm, MovieManager, MovieList,
    ContactForm, ContactManager, ContactList
)

class OrganizerApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        
        # Инициализация менеджеров
        self.contact_manager = ContactManager()
        self.book_manager = BookManager()
        self.movie_manager = MovieManager()
        
        # Индекс текущей редактируемой записи
        self.current_edit_index = None 

    def build(self):
        screen = MDScreen()
        
        # Добавляем верхнюю панель
        toolbar = MDTopAppBar(
            title="Личный органайзер",
            elevation=4,
            pos_hint={"top": 1}
        )
        screen.add_widget(toolbar)
        
        # Создаем навигацию
        bottom_navigation = MDBottomNavigation(
            panel_color=self.theme_cls.primary_color,
            selected_color_background=self.theme_cls.primary_light,
            text_color_active=self.theme_cls.primary_dark,
        )
        
        # Добавляем вкладки
        bottom_navigation.add_widget(self.create_contacts_tab())
        bottom_navigation.add_widget(self.create_books_tab())
        bottom_navigation.add_widget(self.create_movies_tab())
        
        screen.add_widget(bottom_navigation)
        return screen

    def create_contacts_tab(self):
        tab = MDBottomNavigationItem(
            name="contacts",
            text="Контакты",
            icon="account-group",
        )
        
        # Создаем список контактов
        self.contact_list = ContactList(
            manager=self.contact_manager,
            show_form_callback=self.show_contact_dialog
        )
        tab.add_widget(self.contact_list)
        
        return tab

    def create_books_tab(self):
        tab = MDBottomNavigationItem(
            name="books",
            text="Книги",
            icon="book-open-variant",
        )
        
        # Создаем список книг
        self.book_list = BookList(
            manager=self.book_manager,
            show_form_callback=self.show_book_dialog
        )
        tab.add_widget(self.book_list)
        
        return tab

    def create_movies_tab(self):
        tab = MDBottomNavigationItem(
            name="movies",
            text="Фильмы",
            icon="movie-open",
        )
        
        # Создаем список фильмов
        self.movie_list = MovieList(
            manager=self.movie_manager,
            show_form_callback=self.show_movie_dialog
        )
        tab.add_widget(self.movie_list)
        
        return tab

    # Методы для работы с контактами
    def show_contact_dialog(self, index=None):
        if index is not None:
            # Редактирование
            contact = self.contact_manager.get_contacts()[index]
            self.current_edit_index = index
            self.form = ContactForm()
            self.form.set_data(contact)
            title = "Редактировать контакт"
        else:
            # Создание
            self.current_edit_index = None
            self.form = ContactForm()
            title = "Новый контакт"
        
        # Устанавливаем обработчики
        self.form.on_save = self.save_contact
        self.form.on_delete = self.delete_contact
        self.form.on_cancel = lambda: self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title=title,
            type="custom",
            content_cls=self.form,
            radius=[20, 20, 20, 20],
            buttons=self.form.get_buttons(edit_mode=index is not None)
        )
        self.dialog.open()

    def save_contact(self, *args):
        if self.form.is_valid():
            if self.current_edit_index is not None:
                self.contact_manager.update_contact(self.current_edit_index, self.form.get_data())
            else:
                self.contact_manager.add_contact(self.form.get_data())
            self.contact_list.update_list()
            self.dialog.dismiss()

    def delete_contact(self):
        print(f"Удаление контакта с индексом: {self.current_edit_index}")  # Отладочное сообщение
        self.contact_manager.delete_contact(self.current_edit_index)
        self.contact_list.update_list()
        self.dialog.dismiss()

    # Методы для работы с книгами
    def show_book_dialog(self, index=None):
        if index is not None:
            # Редактирование
            book = self.book_manager.get_books()[index]
            self.current_edit_index = index
            self.form = BookForm()
            self.form.set_data(book)
            title = "Редактировать книгу"
        else:
            # Создание
            self.current_edit_index = None
            self.form = BookForm()
            title = "Новая книга"
        
        # Устанавливаем обработчики
        self.form.on_save = self.save_book
        self.form.on_delete = self.delete_book
        self.form.on_cancel = lambda: self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title=title,
            type="custom",
            content_cls=self.form,
            radius=[20, 20, 20, 20],
            buttons=self.form.get_buttons(edit_mode=index is not None)
        )
        self.dialog.open()

    def save_book(self, *args):
        if self.form.is_valid():
            if self.current_edit_index is not None:
                self.book_manager.update_book(self.current_edit_index, self.form.get_data())
            else:
                self.book_manager.add_book(self.form.get_data())
            self.book_list.update_list()
            self.dialog.dismiss()

    def delete_book(self):
        self.book_manager.delete_book(self.current_edit_index)
        self.book_list.update_list()
        self.dialog.dismiss()

    # Методы для работы с фильмами
    def show_movie_dialog(self, index=None):
        if index is not None:
            # Редактирование
            movie = self.movie_manager.get_movies()[index]
            self.current_edit_index = index
            self.form = MovieForm()
            self.form.set_data(movie)
            title = "Редактировать фильм"
        else:
            # Создание
            self.current_edit_index = None
            self.form = MovieForm()
            title = "Новый фильм"
        
        # Устанавливаем обработчики
        self.form.on_save = self.save_movie
        self.form.on_delete = self.delete_movie
        self.form.on_cancel = lambda: self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title=title,
            type="custom",
            content_cls=self.form,
            radius=[20, 20, 20, 20],
            buttons=self.form.get_buttons(edit_mode=index is not None)
        )
        self.dialog.open()

    def save_movie(self, *args):
        if self.form.is_valid():
            if self.current_edit_index is not None:
                self.movie_manager.update_movie(self.current_edit_index, self.form.get_data())
            else:
                self.movie_manager.add_movie(self.form.get_data())
            self.movie_list.update_list()
            self.dialog.dismiss()

    def delete_movie(self):
        self.movie_manager.delete_movie(self.current_edit_index)
        self.movie_list.update_list()
        self.dialog.dismiss()

if __name__ == "__main__":
    OrganizerApp().run() 