from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDIcon, MDLabel
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.button import MDFlatButton, MDRaisedButton

# Список городов
CITIES = [
    "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", 
    "Казань", "Нижний Новгород", "Челябинск", "Самара", 
    "Омск", "Ростов-на-Дону", "Уфа", "Красноярск", "Воронеж", "Пермь", "Волгоград"
]

class ContactForm(MDCard):
    def __init__(self, manager=None, list_widget=None, dialog=None, edit_index=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = "vertical"
        self.spacing = "-20dp"
        self.padding = "16dp"
        self.size_hint = (0.9, None)
        # Высота формы = количество полей * высота поля + отступы
        # 8 полей (титул, имя, фамилия, телефон, город, индекс, адрес, заметки)
        self.height = str(50*(8+2)+25) + 'dp'  # 8 полей + отступы
        self.elevation = 0
        self.radius = [16]
        self.md_bg_color = [1, 1, 1, 1]
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        
        # Сохраняем ссылки на менеджер, список и диалог
        self.manager = manager
        self.list_widget = list_widget
        self.dialog = dialog
        self.edit_index = edit_index
        
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
        # Имя
        self.name_field = MDTextField(
            hint_text="Имя"
        )
        self.add_widget(self._create_field_with_icon("account", self.name_field))
        
        # Фамилия
        self.last_name_field = MDTextField(
            hint_text="Фамилия"
        )
        self.add_widget(self._create_field_with_icon("account", self.last_name_field))

        # Телефон
        self.phone_field = MDTextField(
            hint_text="Телефон"
        )
        self.add_widget(self._create_field_with_icon("phone", self.phone_field))

        # Город
        self.city_field = MDTextField(
            hint_text="Город",
            readonly=True,
            icon_right="chevron-down"
        )
        self.add_widget(self._create_field_with_icon("city", self.city_field))
        
        # Почтовый индекс
        self.postcode_field = MDTextField(
            hint_text="Почтовый индекс"
        )
        self.add_widget(self._create_field_with_icon("map-marker", self.postcode_field))
        
        # Адрес
        self.address_field = MDTextField(
            hint_text="Адрес"
        )
        self.add_widget(self._create_field_with_icon("home", self.address_field))
        
        # Заметки
        self.notes_field = MDTextField(
            hint_text="Заметки",
            multiline=True
        )
        self.add_widget(self._create_field_with_icon("note", self.notes_field))

    def _bind_events(self):
        """Привязка обработчиков событий к полям"""
        self.city_field.bind(on_touch_down=self._show_city_menu)

    def _show_city_menu(self, instance, touch):
        """Показать меню выбора города"""
        if instance.collide_point(*touch.pos):
            menu_items = [
                {
                    "text": city,
                    "viewclass": "OneLineListItem",
                    "on_release": lambda x=city: self._set_field_value(instance, x),
                    "height": dp(48),
                } for city in CITIES
            ]
            self._show_dropdown_menu(instance, menu_items)

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
            "name": self.name_field.text.strip(),
            "last_name": self.last_name_field.text.strip(),
            "phone": self.phone_field.text.strip(),
            "city": self.city_field.text.strip(),
            "postcode": self.postcode_field.text.strip(),
            "address": self.address_field.text.strip(),
            "notes": self.notes_field.text.strip()
        }

    def set_data(self, data):
        """Установить данные формы"""
        self.name_field.text = data.get("name", "")
        self.last_name_field.text = data.get("last_name", "")
        self.phone_field.text = data.get("phone", "")
        self.city_field.text = data.get("city", "")
        self.postcode_field.text = data.get("postcode", "")
        self.address_field.text = data.get("address", "")
        self.notes_field.text = data.get("notes", "")

    def is_valid(self):
        """Проверка валидности данных формы"""
        data = self.get_data()
        return all([
            data["name"],
            data["last_name"],
            data["address"]
        ])

    def _on_text(self, instance, value):
        """Обработчик изменения текста"""
        if value:  # Если есть текст
            instance.hint_text = ""  # Скрываем подсказку
        elif not instance.focus:  # Если нет текста и поле не в фокусе
            instance.hint_text = instance._hint_text  # Восстанавливаем подсказку

    def _on_focus(self, instance, value):
        """Обработчик получения/потери фокуса полем"""
        if value:  # Получение фокуса
            if not hasattr(instance, '_hint_text'):
                instance._hint_text = instance.hint_text
            if not instance.text:  # Только если нет текста
                instance.hint_text = ""
        else:  # Потеря фокуса
            if not instance.text:  # Только если нет текста
                instance.hint_text = instance._hint_text 

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

    def save_data(self, *args):
        """
        Сохранение данных контакта через менеджер
        """
        if not self.is_valid():
            return
            
        contact_data = self.get_data()
        
        # Отключаем кнопку сохранения, чтобы избежать множественных сохранений
        for button in self.dialog.buttons:
            if button.text == "СОХРАНИТЬ":
                button.disabled = True
        
        if self.edit_index is not None:
            # Обновление существующего контакта
            self.manager.update_contact(self.edit_index, contact_data)
        else:
            # Добавление нового контакта
            self.manager.add_contact(contact_data)
            
        # Обновляем список
        if self.list_widget:
            self.list_widget.update_list()
            
        # Закрываем диалог
        if self.dialog:
            self.dialog.dismiss()
            
        # Вызываем колбэк, если он установлен
        if self.on_save:
            self.on_save()
    
    def delete_data(self, *args):
        """
        Удаление контакта через менеджер
        """
        if self.edit_index is not None and self.manager:
            self.manager.delete_contact(self.edit_index)
            
            # Обновляем список
            if self.list_widget:
                self.list_widget.update_list()
                
            # Закрываем диалог
            if self.dialog:
                self.dialog.dismiss()
                
            # Вызываем колбэк, если он установлен
            if self.on_delete:
                self.on_delete()
                
    def cancel(self, *args):
        """
        Отмена редактирования/создания
        """
        if self.dialog:
            self.dialog.dismiss()
            
        # Вызываем колбэк, если он установлен
        if self.on_cancel:
            self.on_cancel() 