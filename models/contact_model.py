from .base import BaseManager

class ContactManager(BaseManager):
    """Менеджер для работы с контактами"""
    
    def __init__(self):
        """Инициализация менеджера контактов"""
        super().__init__("contacts.json")
    
    def add_contact(self, contact):
        """
        Добавление нового контакта
        
        Args:
            contact (dict): Данные контакта
        """
        self.add_item(contact)
    
    def update_contact(self, index, contact):
        """
        Обновление существующего контакта
        
        Args:
            index (int): Индекс контакта
            contact (dict): Новые данные контакта
        """
        self.update_item(index, contact)
    
    def delete_contact(self, index):
        """
        Удаление контакта
        
        Args:
            index (int): Индекс контакта
        """
        self.delete_item(index)
    
    def get_contacts(self):
        """
        Получение списка всех контактов
        
        Returns:
            list: Список контактов
        """
        return self.get_items() 