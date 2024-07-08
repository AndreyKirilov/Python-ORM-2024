import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from datetime import timedelta, date
from main_app.models import Author, Book, Artist, Song, Product, Review, Driver, DrivingLicense, Owner, Car, Registration


def show_all_authors_with_their_books():
    authors = Author.objects.all().order_by('id')
    authors_result = []

    for a in authors:
        books = Book.objects.filter(author=a)

        if books:
            authors_result.append(f"{a.name} has written - {', '.join(b.title for b in books)}!")

    return '\n'.join(authors_result)


def delete_all_authors_without_books():
    Author.objects.filter(book__isnull=True).delete()


def add_song_to_artist(artist_name, song_title):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.add(song)


def get_songs_by_artist(artist_name):
    artist = Artist.objects.get(name=artist_name)

    return artist.songs.all().order_by('-id')


def remove_song_from_artist(artist_name, song_title):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.remove(song)


def calculate_average_rating_for_product_by_name(product_name):
    product = Product.objects.get(name=product_name)
    reviews = product.reviews.all()

    total_rating = sum(r.rating for r in reviews)
    ratings_count = len(reviews)

    average_rating = total_rating / ratings_count
    return average_rating


def get_reviews_with_high_ratings(threshold):
    return Review.objects.filter(rating__gte=threshold)


def get_products_with_no_reviews():
    return Product.objects.filter(reviews__isnull=True).order_by('-name')


def delete_products_without_reviews():
    Product.objects.filter(reviews__isnull=True).delete()


def calculate_licenses_expiration_dates():
    result = []
    licenses = DrivingLicense.objects.all().order_by('-license_number')

    for license in licenses:
        expiration_date = license.issue_date + timedelta(days=365)
        result.append(f"License with number: {license.license_number} expires on {expiration_date}!")

    return '\n'.join(result)


def get_drivers_with_expired_licenses(due_date):
    license_issued_date = due_date - timedelta(days=365)
    drivers = Driver.objects.filter(license__issue_date__gt=license_issued_date)
    return drivers


def register_car_by_owner(owner: Owner):
    registration = Registration.objects.filter(car__isnull=True).first()
    car = Car.objects.filter(registration__isnull=True).first()

    car.owner = owner
    car.save()

    registration.registration_date = date.today()
    registration.car = car
    registration.save()

    return (f"Successfully registered {car.model} to {owner.name} with registration number"
            f" {registration.registration_number}.")
