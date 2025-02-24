from kivymd.uix.list import MDList, ThreeLineIconListItem, IconLeftWidget
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivymd.theming import ThemableBehavior

class BookList(ThemableBehavior, MDBoxLayout):
    def __init__(self, manager, show_form_callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = "vertical"
        self.spacing = "12dp"
        self.padding = ("12dp", "12dp", "12dp", "12dp")
        
        self.manager = manager
        self.show_form_callback = show_form_callback
        
        # Добавляем заголовок для списка книг
        header = MDLabel(
            text="Список книг",
            halign="center",
            size_hint_y=None,
            height="30dp",
            theme_text_color="Primary"
        )
        self.add_widget(header, index=0)
        
        # Создаем прокручиваемый список
        scroll = MDScrollView(size_hint_y=1)
        self.list = MDList(
            spacing="12dp",
            padding=("12dp", "12dp", "12dp", "12dp"),
        )
        scroll.add_widget(self.list)
        self.add_widget(scroll)
        
        # Кнопка добавления и метка количества записей
        button_layout = MDBoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height="48dp",
            padding=("12dp", "0dp", "12dp", "0dp")
        )

        # Сначала добавляем метку с количеством записей (слева)
        self.record_count_label = MDLabel(
            text=f"Количество книг: {len(self.manager.get_books())}",
            halign="left",
            valign="middle"
        )
        button_layout.add_widget(self.record_count_label)

        # Добавляем пустой элемент для создания пространства между меткой и кнопкой
        spacer = MDBoxLayout(size_hint_x=1)
        button_layout.add_widget(spacer)

        # Затем добавляем кнопку (справа)
        button = MDFloatingActionButton(
            icon="plus",
            pos_hint={"center_y": .5},
            elevation=4,
            on_release=lambda x: self.show_form_callback(None)
        )
        button_layout.add_widget(button)

        self.add_widget(button_layout)
        
        # Обновляем список
        self.update_list()

    def update_list(self):
        """Обновление списка книг с группировкой по году"""
        self.list.clear_widgets()
        books = self.manager.get_books()
        self.record_count_label.text = f"Количество книг: {len(books)}"  # Обновляем количество записей
        # Группируем книги по году
        books_by_year = {}
        for book in books:
            # Определяем год для группировки
            end_date = book.get('end_date', '')
            start_date = book.get('start_date', '')
            year = None
            if end_date:
                year = end_date.split('.')[-1]
            elif start_date:
                year = start_date.split('.')[-1]
            if year:
                if year not in books_by_year:
                    books_by_year[year] = []
                books_by_year[year].append(book)

        # Отображаем книги, сгруппированные по году
        for year in sorted(books_by_year.keys(), reverse=True):
            # Добавляем заголовок для года
            year_item = ThreeLineIconListItem(text=year, divider="Full", font_style="H6")
            year_item.height = "30dp"  # Уменьшаем высоту в два раза
            self.list.add_widget(year_item)
            for idx, book in enumerate(books_by_year[year]):
                status_icon = {
                    "План": "book-clock",
                    "Читаю": "book-open-page-variant",
                    "Прочитано": "book-check"
                }.get(book.get("status", ""), "book")

                item = ThreeLineIconListItem(
                    text=book.get("title", ""),
                    secondary_text=f"{book.get('author', '')} • {book.get('genre', '')}",
                    tertiary_text=f"{book.get('status', '')} • {book.get('start_date', '')} - {book.get('end_date', '')}",
                    divider="Full",
                    divider_color=self.theme_cls.divider_color,
                    on_release=lambda x, i=idx: self.show_form_callback(i),
                    font_style="H6"  # Делаем первую строку жирной
                )
                item.height = "60dp"  # Устанавливаем меньшую высоту

                icon = IconLeftWidget(
                    icon=status_icon,
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    pos_hint={"center_y": 1.2}  # Поднимаем иконку еще выше
                )
                item.add_widget(icon)
                self.list.add_widget(item) 