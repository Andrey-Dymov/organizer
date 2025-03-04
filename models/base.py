import json
import os

class BaseManager:
    """Базовый класс для менеджеров данных"""
    
    def __init__(self, file_name):
        """
        Инициализация менеджера
        
        Args:
            file_name (str): Имя файла для хранения данных
        """
        self.items = []
        self.data_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db", file_name)
        self.load_data()
    
    def load_data(self):
        """Загрузка данных из файла"""
        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                self.items = json.load(file)
                print(f"Загружено записей: {len(self.items)}")
        except FileNotFoundError:
            self.items = []
            print("Файл не найден, создаем новый список")
        except json.JSONDecodeError:
            self.items = []
            print("Ошибка чтения файла, создаем новый список")
    
    def save_data(self):
        """Сохранение данных в файл"""
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, "w", encoding="utf-8") as file:
                json.dump(self.items, file, ensure_ascii=False, indent=2)
                print(f"[DEBUG] BaseManager.save_data: сохранено записей: {len(self.items)} в {self.data_file}")
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
    
    def add_item(self, item):
        """Добавление записи"""
        print(f"[DEBUG] BaseManager.add_item: добавление записи в {self.data_file}")
        self.items.append(item)
        self.save_data()
    
    def update_item(self, index, item):
        """Обновление записи"""
        print(f"[DEBUG] BaseManager.update_item: обновление записи с индексом {index} в {self.data_file}")
        self.items[index] = item
        self.save_data()
    
    def delete_item(self, index):
        """Удаление записи"""
        print(f"[DEBUG] BaseManager.delete_item: удаление записи с индексом {index} из {self.data_file}")
        del self.items[index]
        self.save_data()
    
    def get_items(self):
        """Получение всех записей"""
        return self.items 