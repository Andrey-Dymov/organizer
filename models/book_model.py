from .base import BaseManager

class BookManager(BaseManager):
    """Менеджер для работы с книгами"""
    
    def __init__(self):
        """Инициализация менеджера книг"""
        super().__init__("books.json")
    
    def add_book(self, book):
        """
        Добавление новой книги
        
        Args:
            book (dict): Данные книги
        """
        self.add_item(book)
    
    def update_book(self, index, book):
        """
        Обновление существующей книги
        
        Args:
            index (int): Индекс книги
            book (dict): Новые данные книги
        """
        self.update_item(index, book)
    
    def delete_book(self, index):
        """
        Удаление книги
        
        Args:
            index (int): Индекс книги
        """
        self.delete_item(index)
    
    def get_books(self):
        """
        Получение списка всех книг
        
        Returns:
            list: Список книг
        """
        return self.get_items() 