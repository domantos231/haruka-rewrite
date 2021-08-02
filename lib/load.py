from copy import deepcopy
import math


class Pet:
    @property
    def lv(self):
        return 1 + int((-1 + math.sqrt(1 + 2 * self.amt)) / 2)
    

    @property
    def exp(self):
        return self.amt - 2 * self.lv * (self.lv - 1)
    

    def battle_init(self):
        self.hp = deepcopy(self.hp_max)


    def attack(self, target):
        target.damaged(self)
    

    def damaged(self, attacker):
        self.hp -= attacker.atk
        if self.hp < 0:
            self.hp = 0
    

class CommonPet(Pet):
    rarity = "COMMON"
    def load(self):
        self.hp_max = self._base_hp + self.lv * 10
        self.atk = self._base_atk + self.lv


class RarePet(Pet):
    rarity = "RARE"
    def load(self):
        self.hp_max = self._base_hp + self.lv * 15
        self.atk = self._base_atk + self.lv * 2


class EpicPet(Pet):
    rarity = "EPIC"
    def load(self):
        self.hp_max = self._base_hp + self.lv * 20
        self.atk = self._base_atk + self.lv * 3


class LegendaryPet(Pet):
    rarity = "LEGENDARY"
    def load(self):
        self.hp_max = self._base_hp + self.lv * 100
        self.atk = self._base_atk + self.lv * 10


class UnknownPet(Pet):
    rarity = "????"
    def load(self):
        self.hp_max = self._base_hp + self.lv * 1000
        self.atk = self._base_atk + self.lv * 100


class Dog(CommonPet):
    def __init__(self, amt):
        self.img = "🐕"
        self.amt = amt
        self._base_hp = 5000
        self._base_atk = 500


class Cat(CommonPet):
    def __init__(self, amt):
        self.img = "🐈"
        self.amt = amt
        self._base_hp = 4900
        self._base_atk = 510


class Buffalo(CommonPet):
    def __init__(self, amt):
        self.img = "🐂"
        self.amt = amt
        self._base_hp = 5100
        self._base_atk = 490


class Bull(CommonPet):
    def __init__(self, amt):
        self.img = "🐃"
        self.amt = amt
        self._base_hp = 5200
        self._base_atk = 480


class Cow(CommonPet):
    def __init__(self, amt):
        self.img = "🐄"
        self.amt = amt
        self._base_hp = 4800
        self._base_atk = 520


class Pig(CommonPet):
    def __init__(self, amt):
        self.img = "🐖"
        self.amt = amt
        self._base_hp = 5300
        self._base_atk = 470


class DromedaryCamel(CommonPet):
    def __init__(self, amt):
        self.img = "🐪"
        self.amt = amt
        self._base_hp = 4700
        self._base_atk = 530


class Mouse(CommonPet):
    def __init__(self, amt):
        self.img = "🐁"
        self.amt = amt
        self._base_hp = 2000
        self._base_atk = 800


class Rabbit(CommonPet):
    def __init__(self, amt):
        self.img = "🐇"
        self.amt = amt
        self._base_hp = 2000
        self._base_atk = 800


class Rooster(CommonPet):
    def __init__(self, amt):
        self.img = "🐓"
        self.amt = amt
        self._base_hp = 4000
        self._base_atk = 600


class Bird(CommonPet):
    def __init__(self, amt):
        self.img = "🐦"
        self.amt = amt
        self._base_hp = 4000
        self._base_atk = 600


class Duck(CommonPet):
    def __init__(self, amt):
        self.img = "🦆"
        self.amt = amt
        self._base_hp = 4500
        self._base_atk = 550


class Lizard(CommonPet):
    def __init__(self, amt):
        self.img = "🦎"
        self.amt = amt
        self._base_hp = 2500
        self._base_atk = 750


class Fish(CommonPet):
    def __init__(self, amt):
        self.img = "🐟"
        self.amt = amt
        self._base_hp = 2500
        self._base_atk = 750


class Snail(CommonPet):
    def __init__(self, amt):
        self.img = "🐌"
        self.amt = amt
        self._base_hp = 6000
        self._base_atk = 400


class Crab(CommonPet):
    def __init__(self, amt):
        self.img = "🦀"
        self.amt = amt
        self._base_hp = 4400
        self._base_atk = 560


class GuideDog(RarePet):
    def __init__(self, amt):
        self.img = "🦮"
        self.amt = amt
        self._base_hp = 8000
        self._base_atk = 800


class ServiceDog(RarePet):
    def __init__(self, amt):
        self.img = "🐕‍🦺"
        self.amt = amt
        self._base_hp = 8000
        self._base_atk = 800


class Horse(RarePet):
    def __init__(self, amt):
        self.img = "🐎"
        self.amt = amt
        self._base_hp = 8500
        self._base_atk = 750


class Ram(RarePet):
    def __init__(self, amt):
        self.img = "🐏"
        self.amt = amt
        self._base_hp = 7500
        self._base_atk = 850


class Sheep(RarePet):
    def __init__(self, amt):
        self.img = "🐑"
        self.amt = amt
        self._base_hp = 7500
        self._base_atk = 850


class Goat(RarePet):
    def __init__(self, amt):
        self.img = "🐐"
        self.amt = amt
        self._base_hp = 7500
        self._base_atk = 850


class Camel(RarePet):
    def __init__(self, amt):
        self.img = "🐫"
        self.amt = amt
        self._base_hp = 7000
        self._base_atk = 900


class Llama(RarePet):
    def __init__(self, amt):
        self.img = "🦙"
        self.amt = amt
        self._base_hp = 7000
        self._base_atk = 900


class Bat(RarePet):
    def __init__(self, amt):
        self.img = "🦇"
        self.amt = amt
        self._base_hp = 5000
        self._base_atk = 1100


class Skunk(RarePet):
    def __init__(self, amt):
        self.img = "🦨"
        self.amt = amt
        self._base_hp = 5000
        self._base_atk = 1100


class Penguin(RarePet):
    def __init__(self, amt):
        self.img = "🐧"
        self.amt = amt
        self._base_hp = 5500
        self._base_atk = 1050
    

class Dove(RarePet):
    def __init__(self, amt):
        self.img = "🕊️"
        self.amt = amt
        self._base_hp = 5500
        self._base_atk = 1050


class Swan(RarePet):
    def __init__(self, amt):
        self.img = "🦢"
        self.amt = amt
        self._base_hp = 9000
        self._base_atk = 700


class Parrot(RarePet):
    def __init__(self, amt):
        self.img = "🦜"
        self.amt = amt
        self._base_hp = 9000
        self._base_atk = 700


class Turtle(RarePet):
    def __init__(self, amt):
        self.img = "🐢"
        self.amt = amt
        self._base_hp = 13000
        self._base_atk = 300


class Snake(RarePet):
    def __init__(self, amt):
        self.img = "🐍"
        self.amt = amt
        self._base_hp = 4000
        self._base_atk = 1200


class BlowFish(RarePet):
    def __init__(self, amt):
        self.img = "🐡"
        self.amt = amt
        self._base_hp = 5000
        self._base_atk = 1100


class Bee(RarePet):
    def __init__(self, amt):
        self.img = "🐝"
        self.amt = amt
        self._base_hp = 4500
        self._base_atk = 1150


class Poodle(EpicPet):
    def __init__(self, amt):
        self.img = "🐩"
        self.amt = amt
        self._base_hp = 10000
        self._base_atk = 1000


class BlackCat(EpicPet):
    def __init__(self, amt):
        self.img = "🐈‍⬛"
        self.amt = amt
        self._base_hp = 8000
        self._base_atk = 1200


class Tiger(EpicPet):
    def __init__(self, amt):
        self.img = "🐅"
        self.amt = amt
        self._base_hp = 9000
        self._base_atk = 1100


class Leopard(EpicPet):
    def __init__(self, amt):
        self.img = "🐆"
        self.amt = amt
        self._base_hp = 9000
        self._base_atk = 1100


class Elephant(EpicPet):
    def __init__(self, amt):
        self.img = "🐘"
        self.amt = amt
        self._base_hp = 12000
        self._base_atk = 800


class Hippo(EpicPet):
    def __init__(self, amt):
        self.img = "🦛"
        self.amt = amt
        self._base_hp = 11000
        self._base_atk = 900


class Owl(EpicPet):
    def __init__(self, amt):
        self.img = "🦉"
        self.amt = amt
        self._base_hp = 9000
        self._base_atk = 1100


class Peacock(EpicPet):
    def __init__(self, amt):
        self.img = "🦚"
        self.amt = amt
        self._base_hp = 9000
        self._base_atk = 1100


class Crocodile(EpicPet):
    def __init__(self, amt):
        self.img = "🐊"
        self.amt = amt
        self._base_hp = 8500
        self._base_atk = 1150


class Whale(EpicPet):
    def __init__(self, amt):
        self.img = "🐋"
        self.amt = amt
        self._base_hp = 10000
        self._base_atk = 1000


class Dolphin(EpicPet):
    def __init__(self, amt):
        self.img = "🐬"
        self.amt = amt
        self._base_hp = 10000
        self._base_atk = 1000


class Shark(EpicPet):
    def __init__(self, amt):
        self.img = "🦈"
        self.amt = amt
        self._base_hp = 8000
        self._base_atk = 1200


class Octopus(EpicPet):
    def __init__(self, amt):
        self.img = "🐙"
        self.amt = amt
        self._base_hp = 9000
        self._base_atk = 1100


class Squid(EpicPet):
    def __init__(self, amt):
        self.img = "🦑"
        self.amt = amt
        self._base_hp = 9000
        self._base_atk = 1100


class Dragon(LegendaryPet):
    def __init__(self, amt):
        self.img = "🐉"
        self.amt = amt
        self._base_hp = 25000
        self._base_atk = 2500


class Sauropod(LegendaryPet):
    def __init__(self, amt):
        self.img = "🦕"
        self.amt = amt
        self._base_hp = 30000
        self._base_atk = 2000


class TRex(LegendaryPet):
    def __init__(self, amt):
        self.img = "🦖"
        self.amt = amt
        self._base_hp = 20000
        self._base_atk = 3000


class UFO(UnknownPet):
    def __init__(self, amt):
        self.img = "🛸"
        self.amt = amt
        self._base_hp = 200000
        self._base_atk = 20000


PetObjects = (*CommonPet.__subclasses__(), *RarePet.__subclasses__(), *EpicPet.__subclasses__(), *LegendaryPet.__subclasses__(), *UnknownPet.__subclasses__())


def add_pet_data(id, amt):
    return PetObjects[id](amt)


class Player:
    def __init__(self, amt, bank_date, bank, interest, pet, win, total):
        self.amt = amt
        self.bank_date = bank_date
        self.bank = bank
        self.interest = interest
        self.pet = pet
        self.win = win
        self.total = total