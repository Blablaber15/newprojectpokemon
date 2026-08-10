from random import randint
import requests
from datetime import datetime, timedelta

class Pokemon:
    pokemons = {}
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer   
        self.last_feed_time=datetime.now()
        self.pokemon_number = randint(1,1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.color = self.get_colour()
        self.hp=randint(200,400)
        self.power=randint(30,60)
        Pokemon.pokemons[pokemon_trainer] = self

    # Метод для получения картинки покемона через API
    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['sprites']['other']['official-artwork']['front_default'])
        else:
            return "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png"
    
    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"

    #Метод для получения цвета
    def get_colour(self):
            url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return (data['game_indices'][0]['version']['name'])
            else:
                return "red"        
    #Метод атаки бойца
    def attack(self, enemy):
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}"
        else:
            enemy.hp = 0
            return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}! "
    # Метод класса для получения информации
    def info(self):
        return f"Имя твоего покеомона: {self.name},Здоровье твоего покемона:{self.hp},Сила твоего покемона:{self.power}"
    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img
    #Метод голода 
    def feed(self, feed_interval = 20, hp_increase = 10 ):
        current_time = datetime.now() #1 ошибка: datetime.current()  
        delta_time = timedelta(seconds=feed_interval) #2 ошибка:timedelete  и 3 ошибка: hours=feed_interval
        if (current_time - self.last_feed_time) > delta_time:  
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"
        else:
            return f"Следующее время кормления покемона: {self.last_feed_time+delta_time}" #4 ошибка: current_time+delta_time

class Wizard(Pokemon):
    def info(self):
        return super().info()+"Твой покемон имеет клас волшебника"
    def feed(self):
        return super().feed(hp_increase= 20)

class Fighter(Pokemon):
    def attack(self, enemy):
        superpower = randint(5,15)
        self.power += superpower
        result = super().attack(enemy)
        self.power -= superpower
        return result + f"\nБоец применил супер-атаку силой:{superpower} "
    def info(self):
        return super().info()+"Твой покемон имеет класс бойца"
    def feed(self):
        return super().feed(feed_interval=10)
if __name__ == '__main__':
    wizard = Wizard("username1")
    fighter = Fighter("username2")

    print(wizard.info())
    print()
    print(fighter.info())
    print()
    print(fighter.attack(wizard))