from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.pickers import MDDatePicker
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDIcon, MDLabel
from kivymd.uix.selectioncontrol import MDCheckbox

# Константы для фильмов
MOVIE_GENRES = [
    "Боевик", "Комедия", "Драма", "Фантастика", "Триллер",
    "Ужасы", "Мелодрама", "Приключения", "Документальный",
    "Мультфильм", "Детектив", "Фэнтези"
]

MOVIE_TYPES = ["Фильм", "Сериал"]
MOVIE_STATUSES = ["План", "Смотрю", "Просмотрено"]

class MovieForm(MDCard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = "vertical"
        self.spacing = "-20dp"
        self.padding = "16dp"
        self.size_hint = (0.9, None)
        self.height = str(50*(9+2)+25) + 'dp'  # 8 полей + 1 поле даты + отступы
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
        # field.hint_text_mode = "persistent"
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
        # Название фильма
        self.title_field = MDTextField(
            hint_text="Название"
        )
        self.add_widget(self._create_field_with_icon("format-title", self.title_field))
        
        # Год выпуска
        self.year_field = MDTextField(
            hint_text="Год"
        )
        self.add_widget(self._create_field_with_icon("calendar", self.year_field))
        
        # Жанр
        self.genre_field = MDTextField(
            hint_text="Жанр",
            readonly=True,
            icon_right="chevron-down"
        )
        self.add_widget(self._create_field_with_icon("movie-filter", self.genre_field))
        
        # Тип (радиокнопки)
        type_box = MDBoxLayout(
            spacing="12dp",
            adaptive_height=True,
            padding=("0dp", "12dp", "0dp", "12dp")
        )
        
        # Иконка типа
        type_icon = MDIcon(
            icon="movie-open",
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
            pos_hint={"center_y": 0.5}
        )
        type_box.add_widget(type_icon)
        
        # Метка "Тип"
        type_label = MDLabel(
            text="Тип:",
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
            size_hint_x=0.2,
            pos_hint={"center_y": 0.5}
        )
        type_box.add_widget(type_label)
        
        # Контейнер для радиокнопок
        type_radio_box = MDBoxLayout(
            spacing="8dp",
            size_hint_x=1,
            adaptive_height=True
        )
        
        # Контейнер для первой радиокнопки и метки
        film_radio_box = MDBoxLayout(
            spacing="4dp",
            adaptive_height=True,
            size_hint_x=0.5
        )
        
        # Радиокнопка "Фильм"
        self.film_radio = MDCheckbox(
            group="type",
            size_hint=(None, None),
            size=("48dp", "48dp"),
            active=True,
            pos_hint={"center_y": 0.5}
        )
        self.film_radio.bind(active=lambda x, y: self._select_type("Фильм") if y else None)
        film_radio_box.add_widget(self.film_radio)
        
        # Метка "Фильм"
        film_label = MDLabel(
            text="Фильм",
            theme_text_color="Primary",
            pos_hint={"center_y": 0.5}
        )
        film_radio_box.add_widget(film_label)
        
        # Контейнер для второй радиокнопки и метки
        series_radio_box = MDBoxLayout(
            spacing="4dp",
            adaptive_height=True,
            size_hint_x=0.5
        )
        
        # Радиокнопка "Сериал"
        self.series_radio = MDCheckbox(
            group="type",
            size_hint=(None, None),
            size=("48dp", "48dp"),
            active=False,
            pos_hint={"center_y": 0.5}
        )
        self.series_radio.bind(active=lambda x, y: self._select_type("Сериал") if y else None)
        series_radio_box.add_widget(self.series_radio)
        
        # Метка "Сериал"
        series_label = MDLabel(
            text="Сериал",
            theme_text_color="Primary",
            pos_hint={"center_y": 0.5}
        )
        series_radio_box.add_widget(series_label)
        
        # Добавляем контейнеры с радиокнопками в общий контейнер
        type_radio_box.add_widget(film_radio_box)
        type_radio_box.add_widget(series_radio_box)
        
        # Добавляем контейнер с радиокнопками в основной контейнер
        type_box.add_widget(type_radio_box)
        self.add_widget(type_box)
        
        # Текущий выбранный тип (по умолчанию "Фильм")
        self.selected_type = "Фильм"
        
        # Сезон и серия
        episode_box = MDBoxLayout(
            spacing="12dp",
            adaptive_height=True,
            padding=("0dp", "12dp", "0dp", "12dp")
        )
        
        # Иконка эпизода
        episode_icon = MDIcon(
            icon="numeric",
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
            pos_hint={"center_y": 0.5}
        )
        episode_box.add_widget(episode_icon)
        
        # Сезон
        self.season_field = MDTextField(
            hint_text="Сезон",
            input_filter="int",
            readonly=True  # По умолчанию только для чтения
        )
        episode_box.add_widget(self._setup_field(self.season_field))
        
        # Серия
        self.episode_field = MDTextField(
            hint_text="Серия",
            input_filter="int",
            readonly=True  # По умолчанию только для чтения
        )
        episode_box.add_widget(self._setup_field(self.episode_field))
        self.add_widget(episode_box)
        
        # Статус (радиокнопки)
        status_box = MDBoxLayout(
            spacing="12dp",
            adaptive_height=True,
            padding=("0dp", "12dp", "0dp", "12dp")
        )
        
        # Иконка статуса
        status_icon = MDIcon(
            icon="eye-check",
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
        
        for status in MOVIE_STATUSES:
            # Контейнер для радиокнопки и метки
            status_radio_container = MDBoxLayout(
                spacing="4dp",
                adaptive_height=True,
                size_hint_x=1/len(MOVIE_STATUSES)
            )
            
            # Радиокнопка
            radio = MDCheckbox(
                group="status",
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
        
        # Дата просмотра
        self.view_date_field = MDTextField(
            hint_text="Дата просмотра",
            readonly=True,
            icon_right="calendar-check"
        )
        self.add_widget(self._create_field_with_icon("calendar-check", self.view_date_field))

        # Комментарий
        self.comment_field = MDTextField(
            hint_text="Комментарий",
            multiline=True
        )
        self.add_widget(self._create_field_with_icon("comment-text-outline", self.comment_field))
        
    def _bind_events(self):
        """Привязка обработчиков событий к полям"""
        self.genre_field.bind(on_touch_down=self._show_genre_menu)
        self.view_date_field.bind(on_touch_down=self._show_date_picker)

    def _show_genre_menu(self, instance, touch):
        """Показать меню выбора жанра"""
        if instance.collide_point(*touch.pos):
            menu_items = [
                {
                    "text": genre,
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=genre: self._set_field_value(instance, x),
                    "height": dp(48),
                } for genre in MOVIE_GENRES
            ]
            self._show_dropdown_menu(instance, menu_items)

    def _show_date_picker(self, instance, touch):
        """Показать выбор даты"""
        if instance.collide_point(*touch.pos):
            date_dialog = MDDatePicker()
            date_dialog.bind(on_save=lambda instance, value, date_range: self._set_field_value(
                self.view_date_field,
                value.strftime("%d.%m.%Y")
            ))
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
            "year": self.year_field.text.strip(),
            "genre": self.genre_field.text.strip(),
            "type": self.selected_type,
            "season": self.season_field.text.strip() or "0",
            "episode": self.episode_field.text.strip() or "0",
            "status": self.selected_status,
            "comment": self.comment_field.text.strip(),
            "view_date": self.view_date_field.text.strip()
        }

    def set_data(self, data):
        """Установить данные формы"""
        self.title_field.text = data.get("title", "")
        self.year_field.text = data.get("year", "")
        self.genre_field.text = data.get("genre", "")
        
        # Установка типа (Фильм/Сериал)
        type_value = data.get("type", "Фильм")
        self._select_type(type_value)
        
        # Если тип "Сериал", то устанавливаем значения сезона и серии из данных
        # Иначе они уже установлены в _select_type
        if type_value == "Сериал":
            self.season_field.text = data.get("season", "0")
            self.episode_field.text = data.get("episode", "0")
            
        self._select_status(data.get("status", "План"))
        self.comment_field.text = data.get("comment", "")
        self.view_date_field.text = data.get("view_date", "")

    def is_valid(self):
        """Проверка валидности данных формы"""
        data = self.get_data()
        return all([
            data["title"],
            data["year"],
            data["genre"],
            data["type"],
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

    def _select_type(self, type_name):
        """Выбрать тип фильма"""
        self.selected_type = type_name
        if type_name == "Фильм":
            self.film_radio.active = True
            self.series_radio.active = False
            # Делаем поля сезона и серии только для чтения
            self.season_field.readonly = True
            self.episode_field.readonly = True
            # Устанавливаем значения по умолчанию
            self.season_field.text = "0"
            self.episode_field.text = "0"
        else:
            self.film_radio.active = False
            self.series_radio.active = True
            # Делаем поля сезона и серии доступными для редактирования
            self.season_field.readonly = False
            self.episode_field.readonly = False 

    def _select_status(self, status):
        """Выбрать статус фильма"""
        self.selected_status = status
        for s, radio in self.status_radios.items():
            radio.active = (s == status)