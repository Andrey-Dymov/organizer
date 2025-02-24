from kivymd.uix.list import MDList, ThreeLineIconListItem, IconLeftWidget
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivymd.theming import ThemableBehavior

class MovieList(ThemableBehavior, MDBoxLayout):
    def __init__(self, manager, show_form_callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = "vertical"
        self.spacing = "12dp"
        self.padding = ("12dp", "12dp", "12dp", "12dp")
        
        # Добавляем заголовок для списка фильмов в самом начале
        header = MDLabel(
            text="Список фильмов",
            halign="center",
            size_hint_y=None,
            height="30dp",
            theme_text_color="Primary"
        )
        self.add_widget(header)
        
        self.manager = manager
        self.show_form_callback = show_form_callback
        
        # Создаем прокручиваемый список
        scroll = MDScrollView()
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
            text=f"Количество фильмов: {len(self.manager.get_movies())}",
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
        """Обновление списка фильмов с группировкой по году"""
        self.list.clear_widgets()
        movies = self.manager.get_movies()
        self.record_count_label.text = f"Количество фильмов: {len(movies)}"  # Обновляем количество записей
        
        # Группируем фильмы по году
        movies_by_year = {}
        # Сохраняем оригинальные индексы фильмов
        movie_indices = {}
        
        for idx, movie in enumerate(movies):
            # Определяем год для группировки
            view_date = movie.get('view_date', '')
            year = movie.get('year', '')
            group_year = None
            if view_date:
                group_year = view_date.split('.')[-1]
            elif year:
                group_year = year
            if group_year:
                if group_year not in movies_by_year:
                    movies_by_year[group_year] = []
                    movie_indices[group_year] = []
                movies_by_year[group_year].append(movie)
                movie_indices[group_year].append(idx)  # Сохраняем оригинальный индекс

        # Отображаем фильмы, сгруппированные по году
        for year in sorted(movies_by_year.keys(), reverse=True):
            # Добавляем заголовок для года
            year_item = ThreeLineIconListItem(text=year, divider="Full", font_style="H6")
            year_item.height = "30dp"  # Уменьшаем высоту в два раза
            self.list.add_widget(year_item)
            
            for group_idx, movie in enumerate(movies_by_year[year]):
                # Получаем оригинальный индекс фильма
                original_idx = movie_indices[year][group_idx]
                
                # Определяем тип контента (фильм или сериал)
                content_type = movie.get("type", "")
                
                # Выбираем базовую иконку в зависимости от типа контента
                base_icon = "movie" if content_type == "Фильм" else "television-box"
                
                # Добавляем статус к иконке
                status_icon = {
                    "План": f"{base_icon}-clock" if content_type == "Фильм" else "clock-outline",
                    "Смотрю": f"{base_icon}-play" if content_type == "Фильм" else "play-circle-outline",
                    "Просмотрено": f"{base_icon}-check" if content_type == "Фильм" else "check-circle-outline"
                }.get(movie["status"], base_icon)
                
                # Добавляем информацию о сезоне и серии для сериалов
                progress_info = ""
                if content_type == "Сериал" and movie.get("status") == "Смотрю":
                    season = movie.get("season", "0")
                    episode = movie.get("episode", "0")
                    progress_info = f" (S{season}E{episode})"
                
                item = ThreeLineIconListItem(
                    text=movie.get("title", ""),
                    secondary_text=f"{movie.get('year', '')} • {movie.get('genre', '')} • {content_type}",
                    tertiary_text=f"{movie.get('status', '')}{progress_info} • {movie.get('view_date', '')}",
                    divider="Full",
                    divider_color=self.theme_cls.divider_color,
                    on_release=lambda x, i=original_idx: self.show_form_callback(i),  # Используем оригинальный индекс
                    font_style="H6"  # Делаем первую строку жирной
                )
                item.height = "60dp"  # Устанавливаем меньшую высоту
                icon = IconLeftWidget(
                    icon=status_icon,
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    pos_hint={"center_y": 1.5}  # Поднимаем иконку еще выше
                )
                item.add_widget(icon)
                self.list.add_widget(item) 