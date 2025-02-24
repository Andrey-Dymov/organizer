from kivymd.uix.list import MDList, TwoLineIconListItem, IconLeftWidget
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivymd.theming import ThemableBehavior

class ContactList(ThemableBehavior, MDBoxLayout):
    def __init__(self, manager, show_form_callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = "vertical"
        self.spacing = "12dp"
        self.padding = ("12dp", "12dp", "12dp", "12dp")
        
        # Добавляем заголовок для списка контактов в самом начале
        header = MDLabel(
            text="Список контактов",
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
            text=f"Количество контактов: {len(self.manager.get_contacts())}",
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
        """Обновление списка контактов"""
        self.list.clear_widgets()
        contacts = self.manager.get_contacts()
        self.record_count_label.text = f"Количество контактов: {len(contacts)}"  # Обновляем количество записей
        for index, contact in enumerate(contacts):
            # Объединяем имя и фамилию
            full_name = f"{contact.get('name', '')} {contact.get('last_name', '')}".strip()
            phone = contact.get("phone", "")
            city = contact.get("city", "")
            
            # Формируем текст для второй строки
            secondary_text = f"{city}, {contact.get('address', '')}, {contact.get('postcode', '')}".strip(', ')
            
            item = TwoLineIconListItem(
                text=f"{full_name}  {phone}",  # Номер телефона справа в первой строке
                secondary_text=secondary_text,
                divider="Full",
                divider_color=self.theme_cls.divider_color,
                on_release=lambda x, i=index: self.show_form_callback(i),
                _no_ripple_effect=True,  # Отключаем эффект ряби для компактности
                font_style="H6",  # Делаем полное имя жирным
                secondary_font_style="Body2"  # Оставляем вторичный текст обычным
            )
            item.height = "48dp"  # Устанавливаем меньшую высоту
            item.text_color = (0, 0, 0, 1)  # Устанавливаем цвет текста
            item.secondary_text_color = (0.5, 0.5, 0.5, 1)  # Устанавливаем цвет вторичного текста

            icon = IconLeftWidget(
                icon="account",
                theme_text_color="Custom",
                text_color=self.theme_cls.primary_color,
                pos_hint={"center_y": 0.9}  # Поднимаем иконку еще выше
            )
            item.add_widget(icon)
            self.list.add_widget(item) 