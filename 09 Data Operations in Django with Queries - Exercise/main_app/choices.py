from django.db import models


class RoomTypeChoices(models.TextChoices):
    STANDARD = ('ST', 'Standard')
    DELUXE = ('DL', 'Deluxe')
    SUITE = ('SU', 'Suite')


class ClassNameChoices(models.TextChoices):
    MAGE = ('M', 'Mage')
    WARRIOR = ('W', 'Warrior')
    ASSASSIN = ('A', 'Assassin')
    SCOUT = ('S', 'Scout')
