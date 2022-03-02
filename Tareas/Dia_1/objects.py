import random as rnd
from time import sleep

class character():
    """
    Cada uno de los personajes. Tiene los atributos y metodos generales. Los metodos
    say y __repr__ no se usan pero puede importarse este archivo para que el profesor pueda
    crear las clases que quiera y testearlo.
    """
    def __init__(self, name, race='Human', health=100, attck_dmg=15, armor=10,) -> None:
        self.name = name
        self.race = race
        self.health = health
        self.attck_dmg = attck_dmg
        self.armor = armor
    
    def say(self, text):
        print(f'{self.name} says: {text}')
        
    def attack(self, other):
        print(f'\n{self.name} attacks {other.name}.')
        other.damage(self.attck_dmg * (0.7 + 0.6 * rnd.random()))
        
    def damage(self, dmg):
        dmg = round(dmg * (100 - self.armor) / 100)
        dead = ''
        if dmg < 1:
            self.health -= 1
            info = f'Not very effective against {self.name}...'
        else:
            self.health -= round(dmg)
            info = f'{self.name} takes {dmg} damage.'
        if self.health <= 0:
            self.health = 0
            dead = f'\n{self.name} has died.'
        print(f'{info} {self.name} {self.health} HP {dead}')
    
    def __repr__(self) -> str:
        return f'{self.race} {self.name}'
    
    def __str__(self) -> str:
        info = f'Name: {self.name}'
        info += f'\nRace: {self.race}'
        info += f'\nHealth: {self.health}'
        info += f'\nArmor: {self.armor}'
        return info


class enemy(character):
    """
    Los enemigos heredan de la classe character. Además, se sustituye el método __init__.
    Realmente, se complementa este metodo respecto a la clase padre añadiendo un poco de 
    aleatoriedad a los atributos de los enemigos. También se sobreescribe el metodo __str__ para
    que se imprima si este enemigo es el lider.
    """
    def __init__(self, name, race='Human', health=50, attck_dmg=15, armor=10, is_leader=False) -> None:
        super().__init__(name, race, health=health, attck_dmg=attck_dmg, armor=armor)
        self.health += rnd.randint(-10,20)
        self.attck_dmg += rnd.randint(-3,3)
        self.armor += rnd.randint(0, 30)
        self.is_leader = is_leader
        if self.is_leader:
            self.become_leader()
        
        if self.armor > 95:
            self.armor = 95
            
    def become_leader(self):
        self.health = round(self.health * 1.5)
        self.armor = round(self.armor * 1.8)
        self.is_leader = True
    
    def __str__(self):
        if self.is_leader:
            return super().__str__() + '\nThe leader of the gang!'
        else:
            return super().__str__()

class hero(character):
    """
    El jugador de la partida. El __init__ se modifica para que se guarde una variable
    especial (max_health), asi en el metodo heal() no se puede superar esta vida maxima.
    """
    
    def __init__(self, name='Hero', race='Human', health=300, attck_dmg=30, armor=30) -> None:
        super().__init__(name, race, health, attck_dmg, armor)
        self.max_health = self.health
        
    def heal(self):
        self.health += round(0.6 * self.max_health)
        print(f'\n{self.name} heals {round(0.6 * self.max_health)} HP')
        if self.health > self.max_health:
            self.health = self.max_health
        print(f'Current: {self.health} HP')
        
        
class battle():
    """
    Esta classe se utiliza como 'tablero'. Es lo que permite que los personajes 
    interactuen entre si. Se le pasa la informacion del heroe y de los enemigos.
    El método principal es main(), que basicamente tiene el loop principal. En cada
    bucle, se llama al metodo act(), donde el heroe primero actua, y despues los 
    enemigos por orden (los enemigos solo atacan).
    """
    
    def __init__(self, you, enms, enm_race='Human') -> None:
        # Se construye el heroe
        if type(you) == None:
            self.hero = hero()
        elif type(you) == str:
            self.hero = hero(you)
        elif type(you) == dict:
            (hero_name, hero_race), = you.items()
            self.hero = hero(hero_name, hero_race)
        else:
            raise TypeError('you must be a string or a dictionary {"Name": "Race"}')
        
        # Se construye la lista de enemigos
        if type(enms) == dict:
            n = len(enms)
            self.enemies = [enemy(name, enms[name]) for name in enms]
        if type(enms) == int:
            n = enms
            self.enemies = [enemy(f'{enm_race} {i+1}', enm_race) for i in range(n)]
        print(f'\n\nBattle beginning! {len(enms)} enemies have appeared!\n')
        sleep(0.4)
        
        # Se elige un lider de entre los enemigos
        self.leader = rnd.choice(self.enemies)
        self.leader.become_leader()
        self.leader.say(f'{self.hero.name}, I am {self.leader.name} and we will destroy you!')
        sleep(0.7)
    
    def act(self):
        # Turno del heroe
        print("\nIt is your turn.")
        sleep(0.5)
        action = input('[A] Attack\n[H] Heal\n[E] Examine\nWhat do you want to do? > ')
        if action.lower().startswith('a'):
            i_enm = input('Who do you want to attack? > ')
            try:
                i_enm = int(i_enm) - 1
            except ValueError:
                i_enm = -1
            if i_enm < len(self.enemies) and i_enm >= 0:
                self.hero.attack(self.enemies[i_enm])
            else:
                print("\nYou are confused and have attacked air. Next time hoose the number of an enemy.")
        elif action.lower().startswith('h'):
            self.hero.heal()
        elif action.lower().startswith('e'):
            i_enm = input('Which enemy do you want to examine? > ')
            try:
                i_enm = int(i_enm) - 1
            except ValueError:
                i_enm = -1
            if i_enm < len(self.enemies) and i_enm >= 0:
                print(f'\nYou take a closer look at {self.enemies[i_enm].name}')
                print(self.enemies[i_enm])
            else:
                print("\nYou look at nothing, and wonder about your choices in life. Next time choose the number of an enemy.")
        else:
            print(f'\nYou are confused and have tripped down. Next time choose an adecuate action.')
        
        # Comprovamos si algun enemigo ha muerto
        for enemy in self.enemies:
            if enemy.health == 0:
                self.enemies.remove(enemy)        
        
        # Turno de los enemigos
        for enemy in self.enemies:
            sleep(0.8)
            enemy.attack(self.hero)
        
    def main(self):
        # Bucle principal del juego
        while len(self.enemies) > 0 and self.hero.health > 0:
            sleep(1)
            self.stats()
            self.act()
        
        # Final del juego
        if self.hero.health > 0:
            print(f'\n{self.hero.name} has defeated {self.leader.name} and his/her minions!')

        else:
            print(f'\nOh no! {self.leader.name} and his/her minions have defeated {self.hero.name}!')
        sleep(1)
        print('\nThanks for playing!\nBye!')
            
    def stats(self):
        # Imprime la informacion de enemigos y heroe antes de que se actue
        i = 1
        print('\n\n\n\n================ Battleground ================\n')
        for enemy in self.enemies:
            print(f'  [{i}] {enemy.name} HP: {enemy.health}')
            i += 1
        print(f'\n      {self.hero.name} HP: {self.hero.health}')
        print('\n==============================================\n')
        

# Diccionario de enemigos, {Nombre: Raza, ...}
enemies = {'Laura': 'Slug', 
           'Alais': 'Elven', 
           'Sauma': 'Aracnide',
           'Eloi': 'Orc'}

# Diccionario del jugador {Nombre: Raza, ...}
you = {'Miguel': 'Human'}

batt = battle(you, enemies)

batt.main()

input("\nPress Enter to exit")
