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
    """
    Основной класс приложения "Личный органайзер"
    """
    
    def __init__(self, **kwargs):
        """Инициализация приложения"""
        super().__init__(**kwargs)
        # Настройка темы
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        
        # Инициализация менеджеров данных
        self.contact_manager = ContactManager()
        self.book_manager = BookManager()
        self.movie_manager = MovieManager()
        
        # Диалог для форм
        self.dialog = None

    def build(self):
        """Построение основного интерфейса приложения"""
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
        """Создание вкладки контактов"""
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
        """Создание вкладки книг"""
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
        """Создание вкладки фильмов"""
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
        """
        Отображение диалога для создания/редактирования контакта
        
        Args:
            index (int, optional): Индекс редактируемого контакта. None для создания нового.
        """
        # Определяем заголовок диалога
        title = "Редактировать контакт" if index is not None else "Новый контакт"
        
        # Создаем форму с передачей всех необходимых параметров
        self.form = ContactForm(
            manager=self.contact_manager,
            list_widget=self.contact_list,
            edit_index=index
        )
        
        # Если редактируем существующий контакт, загружаем данные
        if index is not None:
            contact = self.contact_manager.get_contacts()[index]
            self.form.set_data(contact)
        
        # Создаем диалог
        self.dialog = MDDialog(
            title=title,
            type="custom",
            content_cls=self.form,
            radius=[20, 20, 20, 20],
            buttons=self.form.get_buttons(edit_mode=index is not None)
        )
        
        # Устанавливаем ссылку на диалог в форме
        self.form.dialog = self.dialog
        
        # Устанавливаем обработчики
        self.form.on_save = self.form.save_data
        self.form.on_delete = self.form.delete_data
        self.form.on_cancel = self.form.cancel
        
        # Открываем диалог
        self.dialog.open()

    # Методы для работы с книгами
    def show_book_dialog(self, index=None):
        """
        Отображение диалога для создания/редактирования книги
        
        Args:
            index (int, optional): Индекс редактируемой книги. None для создания новой.
        """
        # Определяем заголовок диалога
        title = "Редактировать книгу" if index is not None else "Новая книга"
        
        # Создаем форму с передачей всех необходимых параметров
        self.form = BookForm(
            manager=self.book_manager,
            list_widget=self.book_list,
            edit_index=index
        )
        
        # Если редактируем существующую книгу, загружаем данные
        if index is not None:
            book = self.book_manager.get_books()[index]
            self.form.set_data(book)
        
        # Создаем диалог
        self.dialog = MDDialog(
            title=title,
            type="custom",
            content_cls=self.form,
            radius=[20, 20, 20, 20],
            buttons=self.form.get_buttons(edit_mode=index is not None)
        )
        
        # Устанавливаем ссылку на диалог в форме
        self.form.dialog = self.dialog
        
        # Устанавливаем обработчики
        self.form.on_save = self.form.save_data
        self.form.on_delete = self.form.delete_data
        self.form.on_cancel = self.form.cancel
        
        # Открываем диалог
        self.dialog.open()

    # Методы для работы с фильмами
    def show_movie_dialog(self, index=None):
        """
        Отображение диалога для создания/редактирования фильма
        
        Args:
            index (int, optional): Индекс редактируемого фильма. None для создания нового.
        """
        print(f"[DEBUG] OrganizerApp.show_movie_dialog: вызван с индексом {index}")
        
        # Определяем заголовок диалога
        title = "Редактировать фильм" if index is not None else "Новый фильм"
        print(f"[DEBUG] OrganizerApp.show_movie_dialog: заголовок '{title}'")
        
        # Создаем форму с передачей всех необходимых параметров
        self.form = MovieForm(
            manager=self.movie_manager,
            list_widget=self.movie_list,
            edit_index=index
        )
        print("[DEBUG] OrganizerApp.show_movie_dialog: создана форма MovieForm")
        
        # Если редактируем существующий фильм, загружаем данные
        if index is not None:
            movie = self.movie_manager.get_movies()[index]
            self.form.set_data(movie)
            print(f"[DEBUG] OrganizerApp.show_movie_dialog: загружены данные фильма '{movie.get('title', '')}'")
        
        # Создаем диалог
        self.dialog = MDDialog(
            title=title,
            type="custom",
            content_cls=self.form,
            radius=[20, 20, 20, 20],
            buttons=self.form.get_buttons(edit_mode=index is not None)
        )
        print("[DEBUG] OrganizerApp.show_movie_dialog: создан диалог")
        
        # Устанавливаем ссылку на диалог в форме
        self.form.dialog = self.dialog
        print("[DEBUG] OrganizerApp.show_movie_dialog: установлена ссылка на диалог в форме")
        
        # Устанавливаем обработчики
        self.form.on_save = self.form.save_data
        self.form.on_delete = self.form.delete_data
        self.form.on_cancel = self.form.cancel
        print("[DEBUG] OrganizerApp.show_movie_dialog: установлены обработчики событий")
        
        # Открываем диалог
        self.dialog.open()
        print("[DEBUG] OrganizerApp.show_movie_dialog: диалог открыт")

if __name__ == "__main__":
    OrganizerApp().run() 