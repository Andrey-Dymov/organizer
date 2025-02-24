from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.pickers import MDDatePicker
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDIcon, MDLabel
from kivymd.uix.selectioncontrol import MDCheckbox

# Константы для книг
BOOK_GENRES = [
    "Фантастика", "Фэнтези", "Детектив", "Роман", "Приключения",
    "Научная литература", "Психология", "Бизнес", "Биография",
    "Историческая проза", "Ужасы", "Поэзия", "Философия",
    "Классическая литература", "Научная фантастика"
]

BOOK_STATUSES = ["План", "Читаю", "Прочитано"]

class BookForm(MDCard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = "vertical"
        self.spacing = "-20dp"
        self.padding = "16dp"
        self.size_hint = (0.9, None)
        # Высота формы = количество полей * высота поля + отступы
        # 6 одиночных полей (название, автор, жанр, статус, комментарий) + 1 двойное поле (даты)
        # 50dp - высота каждого поля с отступами
        self.height = str(50*(6+2)+25) + 'dp'  # 6 полей + 2 поля дат + отступы
        self.elevation = 0
        self.radius = [16]
        self.md_bg_color = [1, 1, 1, 1]
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        
        # Колбэки для обработки действий
        self.on_save = None
        self.on_delete = None
        self.on_cancel = None
        
        # Создаем все поля формы
        self._create_fields()
        
        # Привязываем обработчики событий
        self._bind_events()

    def _setup_field(self, field):
        """Установка общих параметров для поля"""
        field.mode = "rectangle"
        field.font_size = "18sp"
        field.line_color_normal = (0.8, 0.8, 0.8, 1)
        field.hint_text_color_normal = (0.5, 0.5, 0.5, 1)
        field.text_color_normal = (0, 0, 0, 1)
        field.hint_text = "   " + field.hint_text
        return field

    def _create_field_with_icon(self, icon, field):
        """Создать поле с иконкой слева"""
        box = MDBoxLayout(
            spacing="12dp",
            adaptive_height=True,
            padding=("0dp", "12dp", "0dp", "12dp")
        )
        
        # Иконка
        icon = MDIcon(
            icon=icon,
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
            pos_hint={"center_y": 0.5}
        )
        box.add_widget(icon)
        
        # Поле ввода
        box.add_widget(self._setup_field(field))
        return box

    def _create_fields(self):
        # Название книги
        self.title_field = MDTextField(
            hint_text="Название"
        )
        self.add_widget(self._create_field_with_icon("book", self.title_field))
        
        # Автор
        self.author_field = MDTextField(
            hint_text="Автор"
        )
        self.add_widget(self._create_field_with_icon("account", self.author_field))
        
        # Жанр
        self.genre_field = MDTextField(
            hint_text="Жанр",
            readonly=True,
            icon_right="chevron-down"
        )
        self.add_widget(self._create_field_with_icon("bookmark", self.genre_field))
        
        # Статус (радиокнопки)
        status_box = MDBoxLayout(
            spacing="12dp",
            adaptive_height=True,
            padding=("0dp", "12dp", "0dp", "12dp")
        )
        
        # Иконка статуса
        status_icon = MDIcon(
            icon="clock",
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
            pos_hint={"center_y": 0.5}
        )
        status_box.add_widget(status_icon)
        
        # Метка "Статус"
        status_label = MDLabel(
            text="Статус:",
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
            size_hint_x=0.2,
            pos_hint={"center_y": 0.5}
        )
        status_box.add_widget(status_label)
        
        # Контейнер для радиокнопок статуса
        status_radio_box = MDBoxLayout(
            spacing="8dp",
            size_hint_x=1,
            adaptive_height=True
        )
        
        # Создаем радиокнопки для каждого статуса
        self.status_radios = {}
        
        for status in BOOK_STATUSES:
            # Контейнер для радиокнопки и метки
            status_radio_container = MDBoxLayout(
                spacing="4dp",
                adaptive_height=True,
                size_hint_x=1/len(BOOK_STATUSES)
            )
            
            # Радиокнопка
            radio = MDCheckbox(
                group="book_status",
                size_hint=(None, None),
                size=("48dp", "48dp"),
                active=status == "План",  # По умолчанию "План"
                pos_hint={"center_y": 0.5}
            )
            # Исправляем привязку события - используем замыкание для сохранения значения status
            def make_callback(s):
                return lambda x, v: self._select_status(s) if v else None
            radio.bind(active=make_callback(status))
            status_radio_container.add_widget(radio)
            
            # Метка статуса
            status_label = MDLabel(
                text=status,
                theme_text_color="Primary",
                pos_hint={"center_y": 0.5}
            )
            status_radio_container.add_widget(status_label)
            
            # Сохраняем радиокнопку для дальнейшего использования
            self.status_radios[status] = radio
            
            # Добавляем контейнер в общий бокс
            status_radio_box.add_widget(status_radio_container)
        
        # Добавляем контейнер с радиокнопками в основной контейнер
        status_box.add_widget(status_radio_box)
        self.add_widget(status_box)
        
        # Текущий выбранный статус (по умолчанию "План")
        self.selected_status = "План"
        
        # Даты
        dates_box = MDBoxLayout(
            spacing="12dp",
            adaptive_height=True,
            padding=("0dp", "12dp", "0dp", "12dp")
        )
        
        # Иконка календаря
        date_icon = MDIcon(
            icon="calendar",
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
            pos_hint={"center_y": 0.5}
        )
        dates_box.add_widget(date_icon)
        
        # Дата начала
        self.start_date_field = MDTextField(
            hint_text="Дата начала",
            readonly=True,
            icon_right="calendar"
        )
        dates_box.add_widget(self._setup_field(self.start_date_field))
        
        # Дата окончания
        self.end_date_field = MDTextField(
            hint_text="Дата окончания",
            readonly=True,
            icon_right="calendar"
        )
        dates_box.add_widget(self._setup_field(self.end_date_field))
        
        # Комментарий
        self.comment_field = MDTextField(
            hint_text="Комментарий",
            multiline=True
        )
        self.add_widget(dates_box)

        self.add_widget(self._create_field_with_icon("comment-text-outline", self.comment_field))

    def _bind_events(self):
        """Привязка обработчиков событий к полям"""
        self.genre_field.bind(on_touch_down=self._show_genre_menu)
        self.start_date_field.bind(on_touch_down=self._show_date_picker)
        self.end_date_field.bind(on_touch_down=self._show_date_picker)

    def _show_genre_menu(self, instance, touch):
        """Показать меню выбора жанра"""
        if instance.collide_point(*touch.pos):
            menu_items = [
                {
                    "text": genre,
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=genre: self._set_field_value(instance, x),
                    "height": dp(48),
                } for genre in BOOK_GENRES
            ]
            self._show_dropdown_menu(instance, menu_items)

    def _show_date_picker(self, instance, touch):
        """Показать выбор даты"""
        if not instance.collide_point(*touch.pos):
            return

        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=lambda instance, value, date_range: self._set_field_value(
            self.start_date_field if touch.ud['instance'] == self.start_date_field else self.end_date_field,
            value.strftime("%d.%m.%Y")
        ))
        touch.ud['instance'] = instance  # Сохраняем поле, которое вызвало диалог
        date_dialog.open()

    def _show_dropdown_menu(self, caller, items):
        """Показать выпадающее меню"""
        menu = MDDropdownMenu(
            caller=caller,
            items=items,
            position="auto",
            width_mult=4,
        )
        menu.open()

    def _set_field_value(self, instance, value):
        """Установить значение поля"""
        instance.text = value
        if hasattr(instance, 'menu'):
            instance.menu.dismiss()

    def get_data(self):
        """Получить данные формы"""
        return {
            "title": self.title_field.text.strip(),
            "author": self.author_field.text.strip(),
            "genre": self.genre_field.text.strip(),
            "status": self.selected_status,
            "comment": self.comment_field.text.strip(),
            "start_date": self.start_date_field.text.strip(),
            "end_date": self.end_date_field.text.strip()
        }

    def set_data(self, data):
        """Установить данные формы"""
        self.title_field.text = data.get("title", "")
        self.author_field.text = data.get("author", "")
        self.genre_field.text = data.get("genre", "")
        
        # Устанавливаем статус и обновляем радиокнопки
        status = data.get("status", "План")
        self._select_status(status)
        
        self.comment_field.text = data.get("comment", "")
        self.start_date_field.text = data.get("start_date", "")
        self.end_date_field.text = data.get("end_date", "")

    def is_valid(self):
        """Проверка валидности данных формы"""
        data = self.get_data()
        return all([
            data["title"],
            data["author"],
            data["genre"],
            data["status"]
        ])

    def get_buttons(self, edit_mode=False):
        """Создать кнопки формы"""
        buttons = []
        if edit_mode:
            # Кнопка удаления для режима редактирования
            buttons.append(
                MDFlatButton(
                    text="УДАЛИТЬ",
                    theme_text_color="Custom",
                    text_color=(0.9, 0.1, 0.1, 1),
                    font_size="14sp",
                    on_release=lambda x: self.on_delete() if self.on_delete else None
                )
            )
            
        # Кнопка отмены
        buttons.append(
            MDFlatButton(
                text="ОТМЕНА",
                theme_text_color="Custom",
                text_color=(0.33, 0.33, 0.98, 1),  # primary_color
                font_size="14sp",
                on_release=lambda x: self.on_cancel() if self.on_cancel else None
            )
        )
        
        # Кнопка сохранения
        buttons.append(
            MDRaisedButton(
                text="СОХРАНИТЬ",
                font_size="14sp",
                on_release=lambda x: self.on_save() if self.on_save and self.is_valid() else None
            )
        )
        
        return buttons 

    def _select_status(self, status):
        """Выбор статуса"""
        self.selected_status = status
        for s, radio in self.status_radios.items():
            radio.active = (s == status)

    def _show_dropdown_menu(self, caller, items):
        """Показать выпадающее меню"""
        menu = MDDropdownMenu(
            caller=caller,
            items=items,
            position="auto",
            width_mult=4,
        )
        menu.open()

    def _set_field_value(self, instance, value):
        """Установить значение поля"""
        instance.text = value
        if hasattr(instance, 'menu'):
            instance.menu.dismiss()

    def get_data(self):
        """Получить данные формы"""
        return {
            "title": self.title_field.text.strip(),
            "author": self.author_field.text.strip(),
            "genre": self.genre_field.text.strip(),
            "status": self.selected_status,
            "comment": self.comment_field.text.strip(),
            "start_date": self.start_date_field.text.strip(),
            "end_date": self.end_date_field.text.strip()
        }

    def is_valid(self):
        """Проверка валидности данных формы"""
        data = self.get_data()
        return all([
            data["title"],
            data["author"],
            data["genre"],
            data["status"]
        ])

    def get_buttons(self, edit_mode=False):
        """Создать кнопки формы"""
        buttons = []
        if edit_mode:
            # Кнопка удаления для режима редактирования
            buttons.append(
                MDFlatButton(
                    text="УДАЛИТЬ",
                    theme_text_color="Custom",
                    text_color=(0.9, 0.1, 0.1, 1),
                    font_size="14sp",
                    on_release=lambda x: self.on_delete() if self.on_delete else None
                )
            )
            
        # Кнопка отмены
        buttons.append(
            MDFlatButton(
                text="ОТМЕНА",
                theme_text_color="Custom",
                text_color=(0.33, 0.33, 0.98, 1),  # primary_color
                font_size="14sp",
                on_release=lambda x: self.on_cancel() if self.on_cancel else None
            )
        )
        
        # Кнопка сохранения
        buttons.append(
            MDRaisedButton(
                text="СОХРАНИТЬ",
                font_size="14sp",
                on_release=lambda x: self.on_save() if self.on_save and self.is_valid() else None
            )
        )
        
        return buttons 