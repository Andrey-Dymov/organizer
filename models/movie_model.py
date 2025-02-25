from .base import BaseManager

class MovieManager(BaseManager):
    """Менеджер для работы с фильмами"""
    
    def __init__(self):
        """Инициализация менеджера фильмов"""
        super().__init__("movies.json")
    
    def add_movie(self, movie):
        """
        Добавление нового фильма
        
        Args:
            movie (dict): Данные фильма
        """
        self.add_item(movie)
    
    def update_movie(self, index, movie):
        """
        Обновление существующего фильма
        
        Args:
            index (int): Индекс фильма
            movie (dict): Новые данные фильма
        """
        self.update_item(index, movie)
    
    def delete_movie(self, index):
        """
        Удаление фильма
        
        Args:
            index (int): Индекс фильма
        """
        self.delete_item(index)
    
    def get_movies(self):
        """
        Получение списка всех фильмов
        
        Returns:
            list: Список фильмов
        """
        return self.get_items() 