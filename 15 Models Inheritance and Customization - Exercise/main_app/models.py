from datetime import timedelta, date
from importlib.resources import is_resource

from django.core.exceptions import ValidationError
from django.db import models

from main_app.fields import StudentIDField, MaskedCreditCardField, AnimalIDField, MaskedEmployeeIDField


# Create your models here.
class BaseCharacter(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        abstract = True


class Mage(BaseCharacter):
    elemental_power = models.CharField(max_length=100)
    spellbook_type  = models.CharField(max_length=100)


class Assassin(BaseCharacter):
    weapon_type = models.CharField(max_length=100)
    assassination_technique = models.CharField(max_length=100)


class DemonHunter(BaseCharacter):
    weapon_type = models.CharField(max_length=100)
    demon_slaying_ability  = models.CharField(max_length=100)


class TimeMage(Mage):
    time_magic_mastery = models.CharField(max_length=100)
    temporal_shift_ability  = models.CharField(max_length=100)


class Necromancer(Mage):
    raise_dead_ability = models.CharField(max_length=100)


class ViperAssassin(Assassin):
    venomous_strikes_mastery = models.CharField(max_length=100)
    venomous_bite_ability = models.CharField(max_length=100)


class ShadowbladeAssassin(Assassin):
    shadowstep_ability = models.CharField(max_length=100)


class VengeanceDemonHunter(DemonHunter):
    vengeance_mastery = models.CharField(max_length=100)
    retribution_ability = models.CharField(max_length=100)


class FelbladeDemonHunter(DemonHunter):
    felblade_ability  = models.CharField(max_length=100)


class UserProfile(models.Model):
    username = models.CharField(max_length=70, unique=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)


class Message(models.Model):
    sender = models.ForeignKey(UserProfile, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)

    def mark_as_read(self):
        self.is_read = True

    def reply_to_message(self, reply_content: str):
        message = Message.objects.create(
            sender=self.receiver,
            receiver=self.sender,
            content=reply_content
        )

        return message


    def forward_message(self, receiver: UserProfile):
        message = Message.objects.create(
            sender=self.receiver,
            receiver=receiver,
            content=self.content
        )

        return message


class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = StudentIDField()


class CreditCard(models.Model):
    card_owner = models.CharField(max_length=100)
    card_number = MaskedCreditCardField()


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    number = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField()
    total_guests = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.total_guests > self.capacity:
            raise ValidationError("Total guests are more than the capacity of the room")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

        return f"Room {self.number} created successfully"


class BaseReservation(models.Model):
    room_type = None

    class Meta:
        abstract = True

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def reservation_period(self):
        return (self.end_date - self.start_date).days

    def calculate_total_cost(self):
        return round(self.room.price_per_night * self.reservation_period(), 2)

    def is_reserved(self, start_date, end_date):
        reservations = self.__class__.objects.filter(
            room=self.room,
            start_date__lte=end_date,
            end_date__gte=start_date
        )
        return reservations

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError('Start date cannot be after or in the same end date')

        if self.is_reserved(self.start_date, self.end_date):
            raise ValidationError(f"Room {self.room.number} cannot be reserved")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

        return f"{self.room_type} reservation for room {self.room.number}"


class RegularReservation(BaseReservation):
    room_type = 'Regular'


class SpecialReservation(BaseReservation):
    room_type = 'Special'

    def extend_reservation(self, days: int):
        new_end_date = self.end_date + timedelta(days=days)

        if self.is_reserved(self.start_date, new_end_date):
            raise ValidationError("Error during extending reservation")

        self.end_date = new_end_date
        self.save()

        return f"Extended reservation for room {self.room.number} with {days} days"


class Animal(models.Model):
    name = models.CharField(max_length=100)
    animal_id = AnimalIDField()


class Employee(models.Model):
    name = models.CharField(max_length=100)
    employee_id = MaskedEmployeeIDField()


class Car(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20, unique=True)
    rental_price_per_day = models.DecimalField(max_digits=10, decimal_places=2)


class BaseRental(models.Model):
    rental_type = None

    class Meta:
        abstract = True

    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def rental_period(self):
        return (self.end_date - self.start_date).days

    def calculate_total_cost(self):
        total_cost = round(self.car.rental_price_per_day * self.rental_period(), 2)
        return total_cost

    def check_if_overlaps(self, start_date: date, end_date: date):
        rentals = self.__class__.objects.filter(
            car=self.car,
            start_date__lte=end_date,
            end_date__gte=start_date
        )

        return rentals.exists()

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Start date cannot be after or in the same end date")

        if self.check_if_overlaps(self.start_date, self.end_date):
            raise ValidationError(f"Car {self.car.license_plate} cannot be rented for the selected period")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

        return f"{self.rental_type} rental for car {self.car.license_plate}"

class RegularRental(BaseRental):
    rental_type = 'Regular'


class SpecialRental(BaseRental):
    rental_type = 'Special'

    def extend_rental(self, days: int):
        new_end_date = self.end_date + timedelta(days=days)

        if self.check_if_overlaps(self.start_date, new_end_date):
            raise ValidationError("Error during extending rental")

        self.end_date = new_end_date
        self.save()

        return f"Extended rental for car {self.car.license_plate} with {days} days"







