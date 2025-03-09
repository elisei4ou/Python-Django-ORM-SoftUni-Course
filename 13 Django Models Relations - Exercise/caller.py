import os

import django
from django.utils import timezone

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Artist, Song, Product, Review, DrivingLicense, Driver, Owner, Registration, \
    Car
from datetime import timedelta


# Create queries within functions


def show_all_authors_with_their_books():
    authors = Author.objects.filter(book__isnull=False).distinct().order_by('id')
    output = []
    for author in authors:
        output.append(f'{author.name} has written - {", ".join(b.title for b in author.book_set.all())}!')

    return '\n'.join(output)


def delete_all_authors_without_books():
    Author.objects.filter(book__isnull=True).delete()


def add_song_to_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)
    artist.songs.add(song)


def get_songs_by_artist(artist_name: str):
    artist = Artist.objects.get(name=artist_name)
    return artist.songs.order_by('-id')


def remove_song_from_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.remove(song)


def calculate_average_rating_for_product_by_name(product_name: str):
    product = Product.objects.get(name=product_name)
    return sum(p.rating for p in product.reviews.all()) / product.reviews.count()


def get_reviews_with_high_ratings(threshold: int):
    return Review.objects.filter(rating__gte=threshold)


def get_products_with_no_reviews():
    return Product.objects.filter(reviews__isnull=True).order_by('-name')


def delete_products_without_reviews():
    Product.objects.filter(reviews__isnull=True).delete()


def calculate_licenses_expiration_dates():
    licenses = DrivingLicense.objects.all().order_by('-license_number')
    output = []

    for l in licenses:
        expiration_date = l.issue_date + timedelta(days=365)
        output.append(f"License with number: {l.license_number} expires on {expiration_date}!")

    return '\n'.join(output)


def get_drivers_with_expired_licenses(due_date):
    drivers = Driver.objects.all()
    drivers_with_expired_licenses = []

    for d in drivers:
        if d.license.issue_date + timedelta(days=365) > due_date:
            drivers_with_expired_licenses.append(d)

    return drivers_with_expired_licenses


def register_car_by_owner(owner: Owner):
    registration = Registration.objects.filter(car__isnull=True).first()
    car = Car.objects.filter(registration__isnull=True).first()

    car.registration = registration
    registration.car = car
    registration.registration_date = timezone.now()
    car.owner = owner
    car.save()
    registration.save()

    return f"Successfully registered {car.model} to {car.owner.name} with registration number {registration.registration_number}."
