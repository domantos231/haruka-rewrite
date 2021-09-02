import discord
import math
import os
import random
from PIL import Image
from typing import *
from copy import deepcopy


class MyAnimeListException(Exception):
    pass


class AnimeSearchResult:
    def __init__(self, title, id, url):
        self._title = title
        self._id = id
        self._url = url


    @property
    def title(self):
        return self._title


    @property
    def id(self):
        return self._id


    @property
    def url(self):
        return self._url


class Anime:
    def __init__(self, id, soup):
        self.id = id
        self.soup = soup
    

    @property
    def url(self) -> str:
        return f"https://myanimelist.net/anime/{self.id}"


    @property
    def title(self) -> str:
        obj = self.soup.find(name = "h1")
        return obj.get_text()
    

    @property
    def image_url(self) -> str:
        obj = self.soup.find(name="img", attrs = {"itemprop": "image"})
        return obj.get("data-src")
    

    @property
    def score(self) -> Optional[float]:
        try:
            obj = self.soup.find(name = "span", attrs = {"itemprop": "ratingValue"})
            return float(obj.get_text())
        except:
            return
    

    @property
    def ranked(self) -> Optional[int]:
        try:
            obj = self.soup.find(name = "span", attrs = {"itemprop": "ratingCount"})
            return int(obj.get_text())
        except:
            return
    

    @property
    def popularity(self) -> Optional[int]:
        try:
            obj = self.soup.find(name = "span", attrs = {"class": "numbers popularity"}).strong.extract()
            return int(obj.get_text()[1:])
        except:
            return
    

    @property
    def synopsis(self) -> Optional[str]:
        try:
            obj = self.soup.find(name = "meta", attrs = {"property": "og:description"})
            return obj.get("content")
        except:
            return
    

    @property
    def type(self) -> Optional[str]:
        try:
            obj = self.soup.find(name="span", string="Type:").parent.a.extract()
            return obj.get_text()
        except:
            return


    @property
    def episodes(self) -> Optional[int]:
        try:
            obj = self.soup.find(name="span", string="Episodes:").parent
            obj.span.extract()
            return int(obj.get_text(strip=True))
        except:
            return
    

    @property
    def status(self) -> Optional[str]:
        try:
            obj = self.soup.find(name="span", string="Status:").parent
            obj.span.extract()
            return obj.get_text(strip=True)
        except:
            return
    

    @property
    def aired(self) -> Optional[str]:
        try:
            obj = self.soup.find(name="span", string="Aired:").parent
            obj.span.extract()
            return obj.get_text(strip=True)
        except:
            return
    

    @property
    def broadcast(self) -> Optional[str]:
        try:
            obj = self.soup.find(name="span", string="Broadcast:").parent
            obj.span.extract()
            return obj.get_text(strip=True)
        except:
            return
    

    @property
    def genres(self) -> List[str]:
        genres_ = self.soup.find_all(name="span", attrs = {"itemprop": "genre"})
        return list(genre.get_text() for genre in genres_)
    

    def create_embed(self) -> discord.Embed:
        em = discord.Embed(
            title = self.title,
            description = self.synopsis,
            color = 0x2ECC71,
        )
        em.set_thumbnail(url = self.image_url)
        em.add_field(
            name = "Genres",
            value = ", ".join(self.genres),
            inline = False,
        )
        em.add_field(
            name = "Score",
            value = self.score,
            inline = False,
        )
        em.add_field(
            name = "Aired",
            value = self.aired,
        )
        em.add_field(
            name = "Ranked",
            value = self.ranked,
        )
        em.add_field(
            name = "Popularity",
            value = self.popularity,
        )
        em.add_field(
            name = "Episodes",
            value = self.episodes,
        )
        em.add_field(
            name = "Type",
            value = self.type)
        em.add_field(
            name = "Broadcast",
            value = self.broadcast)
        em.add_field(
            name = "Link reference",
            value = f"[MyAnimeList link]({self.url})",
            inline = False,
        )
        return em


class UrbanSearch:
    def __init__(self, title, meaning, example, url):
        self._title = title
        self._meaning = meaning
        self._example = example
        self._url = url
        
        
    @property
    def title(self):
        return self._title


    @property
    def meaning(self):
        return self._meaning


    @property
    def example(self):
        return self._example


    @property
    def url(self):
        return self._url


    def create_embed(self) -> discord.Embed:
        desc = f"{self.meaning}\n---------------\n{self.example}"
        desc.replace("*", r"\*")
        if len(desc) > 4096:
            desc = desc[:4090] + " [...]"
        em = discord.Embed(
            title = f"{self.title}",
            description = desc,
            url = self.url,
            color = 0x2ECC71,
        )
        em.set_footer(text="From Urban Dictionary")
        return em


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


class EconomyPlayer:
    def __init__(self, amt, time, bank, interest, pet, win, total):
        self.amt = amt
        self.time = time
        self.bank = bank
        self.interest = interest
        self.pet = pet
        self.win = win
        self.total = total


cardlist = [f for f in os.listdir(f"./lib/assets/cards")]


class PlayingCard:
    def __init__(self, *args, **kwargs):
        self._filename = args[0]
        self.id = args[0].split(".")[0]
        self.set = kwargs.pop("set", False)
    

    @property
    def filename(self):
        return self._filename
    

    @property
    def value(self) -> int:
        return int(self.id[:-1])
    

    @property
    def suit(self) -> int:
        return ["a", "b", "c", "d"].index(self.id[-1:])
    

    @property
    def image(self) -> Image:
        if self.set:
            return Image.open("./lib/assets/misc/card_sleeve.png")
        return Image.open(f"./lib/assets/cards/{self.filename}")


class BlackjackCard(PlayingCard):
    @property
    def value(self) -> int:
        value = super().value
        if value < 11 and value > 1:
            return super().value
        elif value > 10:
            return 10
        else:
            return 11


class PlayingHand:
    cardtype = PlayingCard
    def __init__(self, cards: List[PlayingCard]):
        self.cards = cards
    

    @property
    def image(self) -> Image:
        n = len(self.cards)
        empty = Image.new("RGBA", (80 * n, 100))
        for card in enumerate(self.cards):
            empty.paste(card[1].image, (80 * card[0], 0, 80 * card[0] + 80, 100))
        return empty
    

    @property
    def value(self) -> int:
        return sum(card.value for card in self.cards)
    

    def draw(self):
        f = random.choice(cardlist)
        while f in [card.filename for card in self.cards]:
            f = random.choice(cardlist)
        self.cards.append(self.cardtype(f))


class BlackjackHand(PlayingHand):
    cardtype = BlackjackCard
    @property
    def value(self) -> int:
        return self.get_value()[0]


    def get_value(self) -> Tuple[int, bool]:
        point = super().value
        special = False
        for card in self.cards:
            if card.value == 11:
                if point > 21:
                    point -= 10
                else:
                    special = True
        return point, special
